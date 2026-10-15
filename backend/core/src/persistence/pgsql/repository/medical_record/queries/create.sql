INSERT INTO medical_records (id, patient_id, blood_type, known_allergies, chronic_conditions, emergency_contact)
VALUES(:id, :patient_id, :blood_type, :known_allergies, :chronic_conditions, :emergency_contact)
RETURNING *;