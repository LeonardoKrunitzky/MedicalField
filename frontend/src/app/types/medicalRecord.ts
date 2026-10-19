export interface CreateMedicalRecordDTO {
  patient_id: string;
  blood_type: string;
  known_allergies: string;
  chronic_conditions: string;
  emergency_contact: string;
}

export interface MedicalRecord {
  id: string;
  patient_id?: string;
  patient_name?: string;
  blood_type: string;
  known_allergies: string;
  chronic_conditions: string;
  emergency_contact: string;
  created_at?: string;
}

export interface ReadMedicalRecordsResponseDTO {
  items: MedicalRecord[];
}
