'use client';

import React, { useState, useEffect } from 'react';
import { NetworkProvider } from '../context/NetworkContext';
import PhoneFrame from './components/PhoneFrame/PhoneFrame';
import Client from './components/Client/Client';
import Portal from './components/Portal/Portal';
import Login from './components/Login/Login';

export default function HomePage() {
  const [isPortalAuthenticated, setIsPortalAuthenticated] =
    useState<boolean>(false);
  const [viewMode, setViewMode] = useState<'portal' | 'client'>('portal');

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const portalAuth = localStorage.getItem('portal_authenticated');
    if (token && portalAuth === 'true') {
      setIsPortalAuthenticated(true);
    }
  }, []);

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
            🖥️ Visão Portal (Nuvem)
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
          {viewMode === 'portal' && isPortalAuthenticated && (
            <button
              type="button"
              onClick={() => {
                localStorage.removeItem('portal_authenticated');
                setIsPortalAuthenticated(false);
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
              Sair do Portal
            </button>
          )}
        </div>
      </header>

      <main style={{ background: '#f8fafc', minHeight: 'calc(100vh - 60px)' }}>
        {viewMode === 'portal' ? (
          isPortalAuthenticated ? (
            <Portal />
          ) : (
            <Login
              onLoginSuccess={() => {
                localStorage.setItem('portal_authenticated', 'true');
                setIsPortalAuthenticated(true);
              }}
            />
          )
        ) : (
          <PhoneFrame>
            <Client />
          </PhoneFrame>
        )}
      </main>
    </NetworkProvider>
  );
}