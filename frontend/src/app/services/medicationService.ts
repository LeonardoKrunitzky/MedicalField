import { api } from './api';
import type {
  Medication,
  MedicationByAttendance,
  ReadMedicationResponseDTO,
  ReadMedicationByAttendanceResponseDTO,
} from '../types';

export const medicationService = {
  getMedications: async (): Promise<Medication[]> => {
    const res = await api.get<ReadMedicationResponseDTO | Medication[]>(
      '/core/usecases/medication/',
    );
    return Array.isArray(res.data) ? res.data : res.data?.items || [];
  },

  getMedicationsByAttendance: async (
    attendanceId: string,
  ): Promise<MedicationByAttendance[]> => {
    const res = await api.get<
      ReadMedicationByAttendanceResponseDTO | MedicationByAttendance[]
    >(`/core/usecases/medication/${attendanceId}`);

    return Array.isArray(res.data) ? res.data : res.data?.items || [];
  },
};
