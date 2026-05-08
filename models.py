from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="doctor") # doctor, admin
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(Integer) # 1: male, 0: female
    email = Column(String, unique=True)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    predictions = relationship("Prediction", back_populates="patient")

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    
    # Input Features
    age = Column(Float)
    sex = Column(Float)
    cp = Column(Float)
    trestbps = Column(Float)
    chol = Column(Float)
    fbs = Column(Float)
    restecg = Column(Float)
    thalach = Column(Float)
    exang = Column(Float)
    oldpeak = Column(Float)
    slope = Column(Float)
    ca = Column(Float)
    thal = Column(Float)
    
    # Output
    result = Column(Integer) # 0 or 1
    probability = Column(Float)
    risk_level = Column(String) # Low, Medium, High
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    patient = relationship("Patient", back_populates="predictions")

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    message = Column(String)
    is_read = Column(Boolean, default=False)
    severity = Column(String) # High, Critical
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    details = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
