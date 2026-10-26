export interface MedicationItem {
  name: string;
  applied_dose: string;
  standard_dosage?: string;
}

export interface AttendanceReportPayload {
  attendance_id: string;
  patient_name: string;
  patient_document?: string;
  professional_name: string;
  pressure: string;
  heart_rate: number;
  consciousness_level: number;
  triage_protocol: string;
  notes?: string;
  created_at?: string;
  blood_type?: string;
  known_allergies?: string;
  chronic_conditions?: string;
  emergency_contact?: string;
  medications?: MedicationItem[];
}

export interface TracingPayload {
  client_ip: string;
  professional_id: string | number | null;
  http_method: string;
  route: string;
  status_code: number;
  processing_time_ms: number;
}