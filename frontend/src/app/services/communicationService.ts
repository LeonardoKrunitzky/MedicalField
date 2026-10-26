import axios from 'axios';

const communicationApi = axios.create({
  baseURL: process.env.NEXT_PUBLIC_COMMUNICATION_URL || 'http://localhost:3001',
});

communicationApi.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

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
  medications?: {
    name?: string;
    medication_id?: string;
    applied_dose: string;
    standard_dosage?: string;
  }[];
}

export const communicationService = {
  downloadAttendancePdf: async (
    reportData: AttendanceReportPayload
  ): Promise<void> => {
    const res = await communicationApi.post('/generate-pdf', reportData, {
      responseType: 'blob',
    });

    const blob = new Blob([res.data], { type: 'application/pdf' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute(
      'download',
      `Ficha_Atendimento_${reportData.patient_name.replace(/\s+/g, '_')}.pdf`
    );
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
  },

  sendAttendanceEmail: async (
    toEmail: string,
    reportData: AttendanceReportPayload
  ): Promise<void> => {
    await communicationApi.post('/send-email', {
      toEmail,
      reportData,
    });
  },
};