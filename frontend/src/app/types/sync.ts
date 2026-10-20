import { Attendance } from "./attendance";
import { MedicalRecord } from "./medicalRecord";
import { Medication } from "./medication";
import { Patient } from "./patient";

export interface OfflineDataResponseDTO {
  patients?: { items: Patient[] } | Patient[];
  medical_records?: { items: MedicalRecord[] } | MedicalRecord[];
  attendances?: { items: Attendance[] } | Attendance[];
  medications?: { items: Medication[] } | Medication[];
}

export interface LocalCacheData {
  patients: Patient[];
  medicalRecords: MedicalRecord[];
  attendances: Attendance[];
  medications: Medication[];
}