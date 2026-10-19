'use client';

import React from 'react';
import { useForm } from 'react-hook-form';
import { coreService } from '../../services/coreService';
import { LoginRequestDTO } from '../../types';

interface LoginProps {
  onLoginSuccess: () => void;
}

export default function Login({ onLoginSuccess }: LoginProps) {
  const { register, handleSubmit } = useForm<LoginRequestDTO>();

  const onSubmit = async (data: LoginRequestDTO) => {
    try {
      const res = await coreService.login(data);
      localStorage.setItem('access_token', res.access_token);

      try {
        const payload = JSON.parse(atob(res.access_token.split('.')[1]));
        if (payload.sub) {
          localStorage.setItem('professional_id', payload.sub);
        }
      } catch {}

      onLoginSuccess();
    } catch {
      alert('Credenciais inválidas!');
    }
  };

  return (
    <div
      style={{
        maxWidth: 380,
        margin: '100px auto',
        padding: 28,
        background: '#ffffff',
        border: '1px solid #e2e8f0',
        borderRadius: 12,
        color: '#0f172a',
        boxShadow: '0 10px 25px rgba(0,0,0,0.05)',
      }}
    >
      <h2 style={{ marginTop: 0 }}>🔐 Login MedicalField</h2>
      <form
        onSubmit={handleSubmit(onSubmit)}
        style={{ display: 'flex', flexDirection: 'column', gap: 14 }}
      >
        <input
          placeholder="Registro Profissional (ex: CRM12345)"
          {...register('professional_registration', { required: true })}
          style={{
            padding: 10,
            borderRadius: 6,
            border: '1px solid #cbd5e1',
            background: '#fff',
            color: '#0f172a',
          }}
        />
        <input
          type="password"
          placeholder="Senha"
          {...register('password', { required: true })}
          style={{
            padding: 10,
            borderRadius: 6,
            border: '1px solid #cbd5e1',
            background: '#fff',
            color: '#0f172a',
          }}
        />
        <button
          type="submit"
          style={{
            padding: 12,
            background: '#2563eb',
            color: '#fff',
            border: 'none',
            borderRadius: 6,
            fontWeight: 'bold',
            cursor: 'pointer',
          }}
        >
          Entrar
        </button>
      </form>
    </div>
  );
}