SELECT 
    attendances.id,
    patients.name as patient_name,
    professionals.name as professional_name,
    medical_records.id as medical_record_id,
    attendances.pressure,
    attendances.heart_rate,
    attendances.consciousness_level,
    attendances.triage_protocol,
    attendances.notes
    attendances.created_at
    attendances.synchronized_at
FROM attendances
INNER JOIN medical_records ON attendances.medical_record_id = medical_records.id
INNER JOIN patients ON medical_records.patient_id = patients.id
INNER JOIN professionals ON attendances.professional_id = professionals.id
WHERE patients.id = $1