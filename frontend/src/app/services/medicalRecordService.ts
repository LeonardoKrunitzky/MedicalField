import { api } from "./api";
import type {
  CreateMedicalRecordDTO,
  MedicalRecord,
  ReadMedicalRecordsResponseDTO,
} from "../types";

export const medicalRecordService = {
  getMedicalRecords: async (): Promise<MedicalRecord[]> => {
    const res = await api.get<ReadMedicalRecordsResponseDTO | MedicalRecord[]>(
      "/core/usecases/medical-record/",
    );
    return Array.isArray(res.data) ? res.data : res.data?.items || [];
  },

  getMedicalRecordByPatient: async (
    patientId: string,
  ): Promise<MedicalRecord> => {
    const res = await api.get<MedicalRecord>(
      `/core/usecases/medical-record/patient/${patientId}`,
    );
    return res.data;
  },

  getMedicalRecordById: async (recordId: string): Promise<MedicalRecord> => {
    const res = await api.get<MedicalRecord>(
      `/core/usecases/medical-record/record/${recordId}`,
    );
    return res.data;
  },

  createMedicalRecord: async (
    data: CreateMedicalRecordDTO,
  ): Promise<MedicalRecord> => {
    const isOffline = Boolean(data.is_offline);
    const payload = { ...data, is_offline: isOffline };
    const res = await api.post<MedicalRecord>(
      "/core/usecases/medical-record/",
      payload
    );
    return res.data;
  },
};
