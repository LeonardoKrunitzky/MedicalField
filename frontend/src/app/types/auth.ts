export interface LoginRequestDTO {
  professional_registration: string;
  password: string;
}

export interface LoginResponseDTO {
  access_token: string;
}
