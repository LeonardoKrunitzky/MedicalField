import { api } from './api';
import type { LoginRequestDTO, LoginResponseDTO } from '../types';

export const authService = {
  login: async (data: LoginRequestDTO): Promise<LoginResponseDTO> => {
    const res = await api.post<LoginResponseDTO>(
      '/core/usecases/professional/login',
      data,
    );
    return res.data;
  },
};
