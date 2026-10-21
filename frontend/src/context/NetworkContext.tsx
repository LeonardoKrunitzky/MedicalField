'use client';

import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  useRef,
  ReactNode,
} from 'react';
import { coreService } from '../app/services/coreService';
import type { LocalCacheData } from '../app/types';

const OFFLINE_COOKIE_NAME = 'mf_offline_data';

const setCookieData = (name: string, value: LocalCacheData, days = 7) => {
  if (typeof document === 'undefined') return;
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  const serialized = encodeURIComponent(JSON.stringify(value));
  document.cookie = `${name}=${serialized}; expires=${expires}; path=/; SameSite=Lax`;
};

const getCookieData = (name: string): LocalCacheData | null => {
  if (typeof document === 'undefined') return null;
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  if (match) {
    try {
      return JSON.parse(decodeURIComponent(match[2]));
    } catch {
      return null;
    }
  }
  return null;
};

interface NetworkContextType {
  isOnline: boolean;
  setIsOnline: React.Dispatch<React.SetStateAction<boolean>>;
  localCache: LocalCacheData;
  isSyncing: boolean;
  hasPendingOfflineChanges: boolean;
  markOfflineChange: () => void;
  loadOnlineData: () => Promise<void>;
  refreshOfflineCookie: () => Promise<LocalCacheData | undefined>;
  handleManualSync: () => Promise<void>;
}

const NetworkContext = createContext<NetworkContextType | undefined>(undefined);

export const NetworkProvider = ({ children }: { children: ReactNode }) => {
  const [isOnline, setIsOnline] = useState<boolean>(true);
  const [isSyncing, setIsSyncing] = useState<boolean>(false);
  const [hasPendingOfflineChanges, setHasPendingOfflineChanges] =
    useState<boolean>(false);
  const [localCache, setLocalCache] = useState<LocalCacheData>({
    patients: [],
    medicalRecords: [],
    attendances: [],
    medications: [],
  });

  const prevOnlineRef = useRef<boolean>(isOnline);

  
  const loadOnlineData = useCallback(async () => {
    if (typeof window !== 'undefined' && !localStorage.getItem('access_token')) {
      return;
    }
    try {
      const [patients, medicalRecords, attendances, medications] =
        await Promise.all([
          coreService.getPatients(),
          coreService.getMedicalRecords(),
          coreService.getAttendances(),
          coreService.getMedications(),
        ]);
      setLocalCache({ patients, medicalRecords, attendances, medications });
    } catch (error) {
      console.error('Erro ao buscar dados nas rotas online:', error);
    }
  }, []);

  
  const refreshOfflineCookie = useCallback(async () => {
    try {
      const offlineData = await coreService.fetchOfflineData();
      setCookieData(OFFLINE_COOKIE_NAME, offlineData);
      if (!isOnline) {
        setLocalCache(offlineData);
      }
      return offlineData;
    } catch (error) {
      console.error('Erro ao buscar dados do SQLite (fetchOfflineData):', error);
    }
  }, [isOnline]);

  const markOfflineChange = useCallback(() => {
    setHasPendingOfflineChanges(true);
  }, []);

  
  useEffect(() => {
    if (isOnline) {
      
      loadOnlineData();
    } else {
      
      const cookieData = getCookieData(OFFLINE_COOKIE_NAME);
      if (cookieData) {
        setLocalCache(cookieData);
      } else {
        refreshOfflineCookie();
      }
    }
  }, [isOnline, loadOnlineData, refreshOfflineCookie]);

  
  const pullFromServer = useCallback(async () => {
    if (!isOnline) {
      alert('Dispositivo Offline! Mude o seletor para Online para sincronizar.');
      return;
    }
    setIsSyncing(true);
    try {
      await coreService.syncPull();
      const offlineData = await coreService.fetchOfflineData();
      setCookieData(OFFLINE_COOKIE_NAME, offlineData);
      await loadOnlineData();
    } catch (error) {
      console.error('Erro ao executar Pull e salvar no Cookie:', error);
      alert('Erro ao sincronizar dados do PostgreSQL para o SQLite.');
    } finally {
      setIsSyncing(false);
    }
  }, [isOnline, loadOnlineData]);

  
  const pushToServer = useCallback(async () => {
    if (!isOnline) return;
    setIsSyncing(true);
    try {
      await coreService.syncPush();
      await coreService.syncPull();
      const offlineData = await coreService.fetchOfflineData();
      setCookieData(OFFLINE_COOKIE_NAME, offlineData);
      await loadOnlineData();
      setHasPendingOfflineChanges(false);
      alert('Sincronização (SQLite -> PostgreSQL) concluída com sucesso!');
    } catch (error) {
      console.error('Erro ao fazer Push do SQLite para o PostgreSQL:', error);
      alert('Erro ao enviar dados offline para a nuvem.');
    } finally {
      setIsSyncing(false);
    }
  }, [isOnline, loadOnlineData]);

  
  useEffect(() => {
    const transitionedToOnline = !prevOnlineRef.current && isOnline;
    prevOnlineRef.current = isOnline;

    if (transitionedToOnline && hasPendingOfflineChanges) {
      console.log('[Observer] Rede Online restabelecida! Disparando Push do SQLite...');
      pushToServer();
    }
  }, [isOnline, hasPendingOfflineChanges, pushToServer]);

  
  const handleManualSync = async () => {
    if (!isOnline) {
      alert('Você está Offline! Ative o toggle para Online antes de sincronizar.');
      return;
    }
    if (hasPendingOfflineChanges) {
      await pushToServer();
    } else {
      await pullFromServer();
      alert('Sincronização concluída! Dados do SQLite salvos no Cookie.');
    }
  };

  return (
    <NetworkContext.Provider
      value={{
        isOnline,
        setIsOnline,
        localCache,
        isSyncing,
        hasPendingOfflineChanges,
        markOfflineChange,
        loadOnlineData,
        refreshOfflineCookie,
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