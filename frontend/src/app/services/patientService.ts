import { api } from './api';
import type {
  CreatePatientDTO,
  Patient,
  ReadPatientResponseDTO,
} from '../types';

export const patientService = {
  getPatients: async (): Promise<Patient[]> => {
    const res = await api.get<ReadPatientResponseDTO | Patient[]>(
      '/core/usecases/patient/',
    );
    return Array.isArray(res.data) ? res.data : res.data?.items || [];
  },

  getPatientById: async (patientId: string): Promise<Patient> => {
    const res = await api.get<Patient>(`/core/usecases/patient/${patientId}`);
    return res.data;
  },

  createPatient: async (data: CreatePatientDTO): Promise<Patient> => {
    const res = await api.post<Patient>('/core/usecases/patient/', data);
    return res.data;
  },
};
