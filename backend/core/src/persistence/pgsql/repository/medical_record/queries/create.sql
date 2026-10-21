INSERT INTO medical_records (id, patient_id, blood_type, known_allergies, chronic_conditions, emergency_contact, created_at)
VALUES(:id, :patient_id, :blood_type, :known_allergies, :chronic_conditions, :emergency_contact, :created_at)
RETURNING *;