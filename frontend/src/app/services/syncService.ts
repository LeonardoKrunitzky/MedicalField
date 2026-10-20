import { api } from './api';
import type {
  Attendance,
  LocalCacheData,
  MedicalRecord,
  Medication,
  Patient,
} from '../types';
import { OfflineDataResponseDTO } from '../types/sync';

const unwrapItems = <T>(data: { items?: T[] } | T[] | undefined): T[] => {
  if (!data) return [];
  if (Array.isArray(data)) return data;
  return data.items || [];
};

export const syncService = {
  syncPull: async () => {
    const res = await api.post('/core/usecases/core/usecases/sync/pull');
    return res.data;
  },

  syncPush: async () => {
    const res = await api.post('/core/usecases/core/usecases/sync/push');
    return res.data;
  },

  fetchOfflineData: async (): Promise<LocalCacheData> => {
    const res = await api.get<OfflineDataResponseDTO>(
      '/core/usecases/core/usecases/sync/fetchOfflineData',
    );
    const raw = res.data;

    return {
      patients: unwrapItems<Patient>(raw?.patients),
      medicalRecords: unwrapItems<MedicalRecord>(raw?.medical_records),
      attendances: unwrapItems<Attendance>(raw?.attendances),
      medications: unwrapItems<Medication>(raw?.medications),
    };
  },
};