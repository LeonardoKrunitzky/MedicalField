'use client';

import React, { ReactNode } from 'react';
import { useNetwork } from '../../../context/NetworkContext';
import './PhoneFrame.css';

interface PhoneFrameProps {
  children: ReactNode;
}

export default function PhoneFrame({ children }: PhoneFrameProps) {
  const {
    isOnline,
    setIsOnline,
    isSyncing,
    hasPendingOfflineChanges,
    handleManualSync,
  } = useNetwork();

  return (
    <div className="phone-environment">
      <div className="simulator-controls">
        <div className="sim-status">
          <span className={`status-dot ${isOnline ? 'online' : 'offline'}`} />
          <strong>Modo: {isOnline ? 'ONLINE' : 'OFFLINE'}</strong>
        </div>

        <label className="toggle-switch">
          <input
            type="checkbox"
            checked={isOnline}
            onChange={() => setIsOnline(!isOnline)}
          />
          <span className="slider" />
        </label>

        <button
          type="button"
          className="sync-btn"
          onClick={handleManualSync}
          disabled={!isOnline || isSyncing}
        >
          {isSyncing
            ? 'Sincronizando...'
            : hasPendingOfflineChanges
            ? '🔄 Sincronizar (Pendente)'
            : '🔄 Sincronizar (Pull SQLite)'}
        </button>
      </div>

      <div className="phone-mockup">
        <div className="phone-notch" />
        <div className="phone-statusbar">
          <span>09:41</span>
          <span>{isOnline ? '📶 5G' : '✈️ Offline'}</span>
        </div>

        <div className="phone-screen">{children}</div>

        <div className="phone-home-indicator" />
      </div>
    </div>
  );
}