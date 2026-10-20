import type { CreateAttendanceMedicationDTO } from './medication';

export interface CreateAttendanceDTO {
  medical_record_id: string;
  professional_id?: string;
  patient_id: string;
  pressure: string;
  heart_rate: number;
  consciousness_level: number;
  triage_protocol: string;
  notes?: string;
  is_offline?: boolean;
  medications?: CreateAttendanceMedicationDTO[];
}

export interface Attendance {
  id: string;
  patient_id: string;
  patient_name: string;
  medical_record_id: string;
  professional_name: string;
  pressure: string;
  heart_rate: number;
  consciousness_level: number;
  triage_protocol: string;
  notes?: string;
  created_at: string;
}

export interface ReadAttendanceResponseDTO {
  items: Attendance[];
}
