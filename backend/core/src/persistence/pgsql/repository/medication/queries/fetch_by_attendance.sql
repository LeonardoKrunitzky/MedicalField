SELECT 
    medications.id,
    medications.name,
    medications.standard_dosage,
    attendance_medications.applied_dose,
    attendance_medications.applied_at
FROM attendance_medications
INNER JOIN medications ON attendance_medications.medication_id = medications.id
WHERE attendance_id = :attendance_id