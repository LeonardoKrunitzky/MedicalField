import type { CreatePatientDTO } from './patient';
import type { CreateMedicalRecordDTO } from './medicalRecord';
import type { CreateAttendanceDTO } from './attendance';

export type OutboxOperationType = 'PATIENT' | 'MEDICAL_RECORD' | 'ATTENDANCE';

export interface OutboxItem {
  tempId: string;
  type: OutboxOperationType;
  payload: CreatePatientDTO | CreateMedicalRecordDTO | CreateAttendanceDTO;
  createdAt: string;
}

export interface LocalCacheData {
  patients: import('./patient').Patient[];
  medicalRecords: import('./medicalRecord').MedicalRecord[];
  medications: import('./medication').Medication[];
}
