'use client';

import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  ReactNode,
} from 'react';
import { coreService } from '../app/services/coreService';
import {
  OutboxItem,
  OutboxOperationType,
  LocalCacheData,
  CreatePatientDTO,
  CreateMedicalRecordDTO,
  CreateAttendanceDTO,
} from '../app/types';

interface NetworkContextType {
  isOnline: boolean;
  setIsOnline: React.Dispatch<React.SetStateAction<boolean>>;
  outboxQueue: OutboxItem[];
  localCache: LocalCacheData;
  isSyncing: boolean;
  enqueueOperation: (
    type: OutboxOperationType,
    payload: CreatePatientDTO | CreateMedicalRecordDTO | CreateAttendanceDTO
  ) => void;
  handleManualSync: () => Promise<void>;
}

const NetworkContext = createContext<NetworkContextType | undefined>(undefined);

export const NetworkProvider = ({ children }: { children: ReactNode }) => {
  const [isOnline, setIsOnline] = useState<boolean>(true);
  const [isSyncing, setIsSyncing] = useState<boolean>(false);
  const [outboxQueue, setOutboxQueue] = useState<OutboxItem[]>([]);
  const [localCache, setLocalCache] = useState<LocalCacheData>({
    patients: [],
    medicalRecords: [],
    medications: [],
  });

  // Carrega dados salvos do localStorage apenas no cliente (evita erro de SSR do Next.js)
  useEffect(() => {
    const savedOutbox = localStorage.getItem('mf_outbox');
    if (savedOutbox) {
      try {
        setOutboxQueue(JSON.parse(savedOutbox));
      } catch {}
    }

    const savedCache = localStorage.getItem('mf_cache');
    if (savedCache) {
      try {
        setLocalCache(JSON.parse(savedCache));
      } catch {}
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('mf_outbox', JSON.stringify(outboxQueue));
  }, [outboxQueue]);

  useEffect(() => {
    localStorage.setItem('mf_cache', JSON.stringify(localCache));
  }, [localCache]);

  const enqueueOperation = (
    type: OutboxOperationType,
    payload: CreatePatientDTO | CreateMedicalRecordDTO | CreateAttendanceDTO
  ) => {
    const tempId = crypto.randomUUID();
    const item: OutboxItem = {
      tempId,
      type,
      payload,
      createdAt: new Date().toISOString(),
    };

    setOutboxQueue((prev) => [...prev, item]);

    if (type === 'PATIENT') {
      const p = payload as CreatePatientDTO;
      setLocalCache((prev) => ({
        ...prev,
        patients: [...prev.patients, { id: tempId, name: p.name, document: p.document }],
      }));
    } else if (type === 'MEDICAL_RECORD') {
      const mr = payload as CreateMedicalRecordDTO;
      setLocalCache((prev) => ({
        ...prev,
        medicalRecords: [...prev.medicalRecords, { id: tempId, ...mr }],
      }));
    }
  };

  // Baixa os catálogos  para o cache local do dispositivo
  const pullFromServer = useCallback(async () => {
    if (!isOnline) {
      alert('Dispositivo Offline! Mude o seletor para Online para sincronizar.');
      return;
    }
    setIsSyncing(true);
    try {
      const [patients, medicalRecords, medications] = await Promise.all([
        coreService.getPatients(),
        coreService.getMedicalRecords(),
        coreService.getMedications(),
      ]);
      setLocalCache({ patients, medicalRecords, medications });
    } catch (error) {
      console.error('Erro ao baixar catálogo:', error);
    } finally {
      setIsSyncing(false);
    }
  }, [isOnline]);

  // Envia a fila Outbox acumulada em modo Offline para o servidor
  const pushOutboxToServer = useCallback(async () => {
    if (!isOnline || outboxQueue.length === 0) return;

    setIsSyncing(true);
    console.log('[Observer] Conectividade Online! Enviando fila Outbox...');

    const remainingQueue: OutboxItem[] = [];

    for (const item of outboxQueue) {
      try {
        if (item.type === 'PATIENT') {
          await coreService.createPatient(item.payload as CreatePatientDTO);
        } else if (item.type === 'MEDICAL_RECORD') {
          await coreService.createMedicalRecord(item.payload as CreateMedicalRecordDTO);
        } else if (item.type === 'ATTENDANCE') {
          await coreService.createAttendance(item.payload as CreateAttendanceDTO);
        }
      } catch (err) {
        console.error(`Falha ao sincronizar ${item.type}:`, err);
        remainingQueue.push(item);
      }
    }

    setOutboxQueue(remainingQueue);
    await pullFromServer();
    setIsSyncing(false);

    if (remainingQueue.length === 0) {
      alert('Sincronização automática concluída com sucesso!');
    }
  }, [isOnline, outboxQueue, pullFromServer]);

  // ====================================================================
  // PADRÃO OBSERVER: Observa a transição de `isOnline` para disparar sync
  // ====================================================================
  useEffect(() => {
    if (isOnline && outboxQueue.length > 0) {
      pushOutboxToServer();
    }
  }, [isOnline, outboxQueue.length, pushOutboxToServer]);

  const handleManualSync = async () => {
    if (!isOnline) {
      alert('Você está Offline! Ative o toggle para Online antes de sincronizar.');
      return;
    }
    if (outboxQueue.length > 0) {
      await pushOutboxToServer();
    } else {
      await pullFromServer();
      alert('Dados sincronizados a partir do Portal com sucesso!');
    }
  };

  return (
    <NetworkContext.Provider
      value={{
        isOnline,
        setIsOnline,
        outboxQueue,
        localCache,
        isSyncing,
        enqueueOperation,
        handleManualSync,
      }}
    >
      {children}
    </NetworkContext.Provider>
  );
};

export const useNetwork = (): NetworkContextType => {
  const context = useContext(NetworkContext);
  if (!context) {
    throw new Error('useNetwork deve ser usado dentro de um NetworkProvider');
  }
  return context;
};