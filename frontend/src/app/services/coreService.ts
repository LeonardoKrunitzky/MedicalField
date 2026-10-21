import { attendanceService } from './attendanceService';
import { authService } from './authService';
import { medicalRecordService } from './medicalRecordService';
import { medicationService } from './medicationService';
import { patientService } from './patientService';
import { syncService } from './syncService';
import type {
  Attendance,
  CreateAttendanceDTO,
  CreateMedicalRecordDTO,
  CreatePatientDTO,
  LocalCacheData,
  LoginRequestDTO,
  LoginResponseDTO,
  MedicalRecord,
  Medication,
  MedicationByAttendance,
  Patient,
} from '../types';

export const coreService = {
  login: async (data: LoginRequestDTO): Promise<LoginResponseDTO> =>
    authService.login(data),

  getPatients: async (): Promise<Patient[]> => patientService.getPatients(),
  getPatientById: async (patientId: string): Promise<Patient> =>
    patientService.getPatientById(patientId),
  createPatient: async (data: CreatePatientDTO): Promise<Patient> =>
    patientService.createPatient(data),

  getMedicalRecords: async (): Promise<MedicalRecord[]> =>
    medicalRecordService.getMedicalRecords(),
  getMedicalRecordByPatient: async (patientId: string): Promise<MedicalRecord> =>
    medicalRecordService.getMedicalRecordByPatient(patientId),
  getMedicalRecordById: async (recordId: string): Promise<MedicalRecord> =>
    medicalRecordService.getMedicalRecordById(recordId),
  createMedicalRecord: async (
    data: CreateMedicalRecordDTO,
  ): Promise<MedicalRecord> => medicalRecordService.createMedicalRecord(data),

  getMedications: async (): Promise<Medication[]> =>
    medicationService.getMedications(),
  getMedicationsByAttendance: async (
    attendanceId: string,
  ): Promise<MedicationByAttendance[]> =>
    medicationService.getMedicationsByAttendance(attendanceId),

  getAttendances: async (): Promise<Attendance[]> =>
    attendanceService.getAttendances(),
  getAttendancesByPatient: async (patientId: string): Promise<Attendance[]> =>
    attendanceService.getAttendancesByPatient(patientId),
  createAttendance: async (data: CreateAttendanceDTO): Promise<Attendance> =>
    attendanceService.createAttendance(data),

  syncPull: async () => syncService.syncPull(),
  syncPush: async () => syncService.syncPush(),
  fetchOfflineData: async (): Promise<LocalCacheData> =>
    syncService.fetchOfflineData(),
};