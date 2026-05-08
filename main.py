from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, auth, database, prediction_engine, websocket_manager
from typing import List
import datetime

# Create Database Tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Heart Disease Prediction API")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Auth Dependency
def get_current_user(token: str, db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except auth.JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == token_data.email).first()
    if user is None:
        raise credentials_exception
    return user

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(full_name=user.full_name, email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(form_data: schemas.LoginRequest, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "user": {"full_name": user.full_name, "email": user.email, "role": user.role}}

@app.post("/predict", response_model=schemas.PredictionResponse)
async def predict_heart_disease(input_data: schemas.PredictionInput, patient_id: int, db: Session = Depends(database.get_db)):
    # 1. Get Prediction
    features = [
        input_data.age, input_data.sex, input_data.cp, input_data.trestbps,
        input_data.chol, input_data.fbs, input_data.restecg, input_data.thalach,
        input_data.exang, input_data.oldpeak, input_data.slope, input_data.ca,
        input_data.thal
    ]
    
    result = prediction_engine.heart_model.predict(features)
    
    # 2. Save Prediction to DB
    new_prediction = models.Prediction(
        patient_id=patient_id,
        **input_data.dict(),
        result=result["result"],
        probability=result["probability"],
        risk_level=result["risk_level"]
    )
    db.add(new_prediction)
    
    # 3. Handle Alerts
    if result["risk_level"] == "High":
        new_alert = models.Alert(patient_id=patient_id, message=f"High Risk Detected for patient {patient_id}", severity="High")
        db.add(new_alert)
        await websocket_manager.manager.broadcast({"type": "ALERT", "message": f"High risk detected for patient!", "patient_id": patient_id})
    
    db.commit()
    return result

@app.get("/history/{patient_id}", response_model=List[schemas.PredictionHistory])
def get_prediction_history(patient_id: int, db: Session = Depends(database.get_db)):
    return db.query(models.Prediction).filter(models.Prediction.patient_id == patient_id).all()

@app.get("/patients")
def list_patients(db: Session = Depends(database.get_db)):
    return db.query(models.Patient).all()

@app.post("/patients")
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(database.get_db)):
    # Check if patient with this email already exists
    existing_patient = db.query(models.Patient).filter(models.Patient.email == patient.email).first()
    if existing_patient:
        return existing_patient
        
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@app.get("/predictions", response_model=List[schemas.PredictionWithPatient])
def get_all_predictions(db: Session = Depends(database.get_db)):
    predictions = db.query(models.Prediction, models.Patient.name).join(models.Patient).all()
    result = []
    for pred, name in predictions:
        p_dict = {c.name: getattr(pred, c.name) for c in pred.__table__.columns}
        p_dict["patient_name"] = name
        result.append(p_dict)
    return result

@app.get("/analytics/stats", response_model=schemas.AnalyticsStats)
def get_analytics_stats(db: Session = Depends(database.get_db)):
    predictions = db.query(models.Prediction).all()
    if not predictions:
        return {
            "risk_distribution": {"High": 0, "Medium": 0, "Low": 0},
            "age_distribution": {},
            "total_predictions": 0,
            "average_probability": 0
        }
    
    total = len(predictions)
    risk_dist = {"High": 0, "Medium": 0, "Low": 0}
    age_dist = {}
    monthly_trends = {}
    total_prob = 0
    
    for p in predictions:
        risk_dist[p.risk_level] = risk_dist.get(p.risk_level, 0) + 1
        total_prob += p.probability
        
        # Age group
        age_group = f"{int(p.age // 10) * 10}-{(int(p.age // 10) * 10) + 9}"
        age_dist[age_group] = age_dist.get(age_group, 0) + 1
        
        # Monthly trend
        month = p.created_at.strftime("%b")
        if month not in monthly_trends:
            monthly_trends[month] = {"sum": 0, "count": 0}
        monthly_trends[month]["sum"] += p.probability
        monthly_trends[month]["count"] += 1
        
    # Format monthly trends for frontend
    final_trends = {m: (v["sum"] / v["count"]) for m, v in monthly_trends.items()}
    
    return {
        "risk_distribution": risk_dist,
        "age_distribution": age_dist,
        "monthly_trends": final_trends,
        "total_predictions": total,
        "average_probability": total_prob / total if total > 0 else 0
    }

@app.delete("/predictions/{prediction_id}")
def delete_prediction(prediction_id: int, db: Session = Depends(database.get_db)):
    prediction = db.query(models.Prediction).filter(models.Prediction.id == prediction_id).first()
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    db.delete(prediction)
    db.commit()
    return {"message": "Prediction deleted successfully"}

import chat_engine

@app.post("/chat")
def chat(request: schemas.ChatRequest):
    response = chat_engine.chat_engine.get_response(request.query)
    return {"response": response}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Echo or handle client messages if needed
    except WebSocketDisconnect:
        websocket_manager.manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
