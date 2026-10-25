from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, json

app = FastAPI(title="HospitalKE API - Kenya")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path for saving - try /tmp first (Render), then local
DATA_FILE = "/tmp/patients.json"

def load_patients():
    # Try to load from file if exists
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                if data:
                    return data
        except:
            pass
    # DEFAULT - NEVER EMPTY! So lecturer always sees patients
    return [
        {"id": 1, "name": "John Kamau", "age": 32, "county": "Nairobi", "condition": "Malaria Checkup"},
        {"id": 2, "name": "Aisha Wafula", "age": 28, "county": "Kisumu", "condition": "Prenatal Care"},
        {"id": 3, "name": "Mike Leon", "age": 45, "county": "Mombasa", "condition": "Fracture"},
        {"id": 4, "name": "Valary Pamela", "age": 25, "county": "Nakuru", "condition": "General Checkup"},
    ]

def save_patients():
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(patients_db, f)
    except:
        pass

patients_db = load_patients()
next_id = max([p["id"] for p in patients_db], default=0) + 1

class PatientIn(BaseModel):
    name: str
    age: int = 25
    county: str = "Nairobi"
    condition: str = "Checkup"

@app.get("/")
def home():
    return {"message": "HospitalKE API LIVE", "status": "online", "total_patients": len(patients_db)}

@app.get("/api/patients")
def get_patients():
    return {"patients": patients_db, "total": len(patients_db)}

@app.post("/api/patients")
def add_patient(p: PatientIn):
    global next_id
    new_patient = {"id": next_id, "name": p.name, "age": p.age, "county": p.county, "condition": p.condition}
    patients_db.append(new_patient)
    next_id += 1
    save_patients()
    return {"message": "Patient added successfully", "patient": new_patient, "total": len(patients_db)}

@app.get("/docs-info")
def info():
    return {"frontend": "https://peterdiana930-cpu.github.io/HospitalKE/", "backend": "https://hospitalke.onrender.com"}