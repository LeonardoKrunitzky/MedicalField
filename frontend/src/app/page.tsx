'use client';

import React, { useState, useEffect } from 'react';
import { NetworkProvider } from '../context/NetworkContext';
import PhoneFrame from './components/PhoneFrame/PhoneFrame';
import Client from './components/Client/Client';
import Portal from './components/Portal/Portal';
import Login from './components/Login/Login';

export default function HomePage() {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [viewMode, setViewMode] = useState<'portal' | 'client'>('client');

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  if (!isAuthenticated) {
    return <Login onLoginSuccess={() => setIsAuthenticated(true)} />;
  }

  return (
    <NetworkProvider>
      <header
        style={{
          height: 60,
          background: '#090d16',
          color: '#fff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 24px',
        }}
      >
        <strong>MedicalField — Simulador Arquitetural</strong>
        <div style={{ display: 'flex', gap: 10 }}>
          <button
            type="button"
            onClick={() => setViewMode('portal')}
            style={{
              padding: '8px 16px',
              borderRadius: 6,
              border: 'none',
              cursor: 'pointer',
              background: viewMode === 'portal' ? '#2563eb' : '#334155',
              color: '#fff',
            }}
          >
            🖥️ Visão Portal
          </button>
          <button
            type="button"
            onClick={() => setViewMode('client')}
            style={{
              padding: '8px 16px',
              borderRadius: 6,
              border: 'none',
              cursor: 'pointer',
              background: viewMode === 'client' ? '#2563eb' : '#334155',
              color: '#fff',
            }}
          >
            📱 Visão Cliente (App Socorrista)
          </button>
          <button
            type="button"
            onClick={() => {
              localStorage.removeItem('access_token');
              setIsAuthenticated(false);
            }}
            style={{
              padding: '8px 12px',
              borderRadius: 6,
              border: 'none',
              background: '#dc2626',
              color: '#fff',
              cursor: 'pointer',
            }}
          >
            Sair
          </button>
        </div>
      </header>

      <main style={{ background: '#f8fafc', minHeight: 'calc(100vh - 60px)' }}>
        {viewMode === 'portal' ? (
          <Portal />
        ) : (
          <PhoneFrame>
            <Client />
          </PhoneFrame>
        )}
      </main>
    </NetworkProvider>
  );
}