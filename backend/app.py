from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

patients_db = []

@app.route('/')
def home():
    return jsonify({"message": "Welcome to HospitalKE Pro - Hospital is Live!", "status": "ok", "patients": len(patients_db)})

@app.route('/health')
def health():
    return jsonify({"status": "HospitalKE is running!"})

@app.route('/api/patients', methods=['GET'])
def get_patients():
    return jsonify({"patients": patients_db, "total": len(patients_db)})

@app.route('/api/patients', methods=['POST'])
def add_patient():
    data = request.get_json()
    patient = {"id": len(patients_db) + 1, "name": data.get("name", "Unknown"), "age": data.get("age", "")}
    patients_db.append(patient)
    return jsonify({"message": "Patient added", "patient": patient})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)