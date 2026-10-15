WITH inserted_attendance AS (
    INSERT INTO attendances (
        id,
        medical_record_id,
        professional_id,
        patient_id,
        pressure,
        heart_rate,
        consciousness_level,
        triage_protocol,
        notes
    )
    VALUES (
        :id,
        :medical_record_id,
        :professional_id,
        :patient_id,
        :pressure,
        :heart_rate,
        :consciousness_level,
        :triage_protocol,
        :notes
    )
    RETURNING
        id,
        medical_record_id,
        professional_id,
        patient_id,
        created_at,
        pressure,
        heart_rate,
        consciousness_level,
        triage_protocol,
        notes,
        synchronized_at
),
inserted_medications AS (
    INSERT INTO attendance_medications (
        id,
        attendance_id,
        medication_id,
        applied_dose,
        applied_at
    )
    SELECT
        CAST(med.id AS UUID),
        ia.id,
        med.medication_id,
        med.applied_dose,
        CAST(med.applied_at AS TIMESTAMP WITH TIME ZONE)
    FROM inserted_attendance ia
    CROSS JOIN jsonb_to_recordset(CAST(:medications AS jsonb)) AS med(
        id UUID,
        medication_id UUID,
        applied_dose VARCHAR,
        applied_at VARCHAR        
    )
)
SELECT * FROM inserted_attendance;