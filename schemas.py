from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    role: Optional[str] = "doctor"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class PredictionInput(BaseModel):
    age: float
    sex: float
    cp: float
    trestbps: float
    chol: float
    fbs: float
    restecg: float
    thalach: float
    exang: float
    oldpeak: float
    slope: float
    ca: float
    thal: float

class PatientCreate(BaseModel):
    name: str
    age: int
    gender: int
    email: EmailStr
    phone: str

class PredictionResponse(BaseModel):
    result: int
    probability: float
    risk_level: str
    recommendations: List[str]
    precautions: List[str]
    contributions: List[dict]

class ChatRequest(BaseModel):
    query: str

class PredictionHistory(BaseModel):
    id: int
    patient_id: int
    risk_level: str
    probability: float
    created_at: datetime
    class Config:
        from_attributes = True

class PredictionWithPatient(PredictionHistory):
    patient_name: str

class AnalyticsStats(BaseModel):
    risk_distribution: dict # {"High": 10, "Medium": 5, ...}
    age_distribution: dict # {"20-30": 2, ...}
    monthly_trends: dict # {"Jan": 0.4, ...}
    total_predictions: int
    average_probability: float
