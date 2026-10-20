import { api } from "./api";
import type {
  Attendance,
  CreateAttendanceDTO,
  ReadAttendanceResponseDTO,
} from "../types";

export const attendanceService = {
  getAttendances: async (): Promise<Attendance[]> => {
    const res = await api.get<ReadAttendanceResponseDTO | Attendance[]>(
      "/core/usecases/attendance/",
    );
    return Array.isArray(res.data) ? res.data : res.data?.items || [];
  },

  getAttendancesByPatient: async (patientId: string): Promise<Attendance[]> => {
    const res = await api.get<ReadAttendanceResponseDTO | Attendance[]>(
      `/core/usecases/attendance/${patientId}`,
    );
    return Array.isArray(res.data) ? res.data : res.data?.items || [];
  },

  createAttendance: async (data: CreateAttendanceDTO): Promise<Attendance> => {
    const isOffline = Boolean(data.is_offline);
    const payload = { ...data, is_offline: isOffline };
    const res = await api.post<Attendance>(
      "/core/usecases/attendance/",
      payload,
      { params: { is_offline: isOffline } },
    );
    return res.data;
  },
};
