SELECT 
    medical_records.id,
    patients.name as patient_name,
    medical_records.blood_type,
    medical_records.known_allergies,
    medical_records.chronic_conditions,
    medical_records.emergency_contact,
    medical_records.created_at
FROM medical_records
INNER JOIN patients ON medical_records.patient_id = patients.id;