export interface Medication {
  id: string;
  name: string;
  standard_dosage: string;
  created_at?: string;
}

export interface MedicationByAttendance {
  id: string;
  name: string;
  standard_dosage: string;
  applied_dose: string;
  applied_at: string;
}

export interface ReadMedicationResponseDTO {
  items: Medication[];
}

export interface ReadMedicationByAttendanceResponseDTO {
  items: MedicationByAttendance[];
}

export interface CreateAttendanceMedicationDTO {
  medication_id: string;
  applied_dose: string;
  applied_at: string;
}
