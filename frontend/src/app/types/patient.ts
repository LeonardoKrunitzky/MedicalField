export interface CreatePatientDTO {
  name: string;
  document: string;
  is_offline?: boolean;
  professional_id?: string;
}

export interface Patient {
  id: string;
  name: string;
  document: string;
  created_at?: string;
}

export interface ReadPatientResponseDTO {
  items: Patient[];
}
