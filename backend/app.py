from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="HospitalKE Pro")

# Homepage - This fixes your main link
@app.get("/")
def home():
    return {
        "message": "Welcome to HospitalKE Pro - Hospital is Live!",
        "go_to_docs": "/docs",
        "status": "OK"
    }

# Patient data model
class Patient(BaseModel):
    name: str
    age: int
    phone: str

# Save patients here for now
patients_db = []

@app.get("/patients")
def get_patients():
    return {"patients": patients_db, "total": len(patients_db)}

@app.post("/patients")
def add_patient(patient: Patient):
    patients_db.append(patient)
    return {"message": "Patient added!", "patient": patient}

@app.get("/health")
def health():
    return {"status": "HospitalKE is running!"}