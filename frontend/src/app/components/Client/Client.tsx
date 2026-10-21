'use client';

import React, { useState, useEffect } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { useNetwork } from '../../../context/NetworkContext';
import { coreService } from '../../services/coreService';
import type {
  LoginRequestDTO,
  CreatePatientDTO,
  CreateMedicalRecordDTO,
  CreateAttendanceDTO,
} from '../../types';
import './Client.css';

type TabType = 'attendance' | 'patient' | 'record' | 'sqlite_data';

export default function Client() {
  const [activeTab, setActiveTab] = useState<TabType>('attendance');
  const [isClientAuthenticated, setIsClientAuthenticated] =
    useState<boolean>(false);

  const {
    isOnline,
    localCache,
    markOfflineChange,
    loadOnlineData,
    refreshOfflineCookie,
  } = useNetwork();

  useEffect(() => {
    const clientToken = localStorage.getItem('client_authenticated');
    if (clientToken === 'true' && localStorage.getItem('access_token')) {
      setIsClientAuthenticated(true);
    }
  }, []);

  
  const { register: regLogin, handleSubmit: submitLogin } =
    useForm<LoginRequestDTO>();

  const onClientLogin = async (data: LoginRequestDTO) => {
    try {
      const res = await coreService.login(data);
      localStorage.setItem('access_token', res.access_token);
      localStorage.setItem('client_authenticated', 'true');

      try {
        const payload = JSON.parse(atob(res.access_token.split('.')[1]));
        if (payload.sub) {
          localStorage.setItem('professional_id', payload.sub);
        }
      } catch {}

      setIsClientAuthenticated(true);
      if (isOnline) {
        await loadOnlineData();
      } else {
        await refreshOfflineCookie();
      }
    } catch {
      alert('Credenciais inválidas no aplicativo do Socorrista!');
    }
  };

  const handleClientLogout = () => {
    localStorage.removeItem('client_authenticated');
    setIsClientAuthenticated(false);
  };

  const {
    register: regPatient,
    handleSubmit: submitPatient,
    reset: resetPatient,
  } = useForm<CreatePatientDTO>();

  const onSavePatient = async (data: CreatePatientDTO) => {
    const isOffline = !isOnline;
    try {
      await coreService.createPatient({
        ...data,
        is_offline: isOffline,
      });

      if (isOffline) {
        markOfflineChange();
        await refreshOfflineCookie();
        alert('Offline: Paciente salvo no SQLite!');
      } else {
        await loadOnlineData();
        alert('Online: Paciente salvo no PostgreSQL!');
      }
      resetPatient();
    } catch (e: any) {
      alert(
        'Erro ao cadastrar paciente: ' +
          (e.response?.data?.detail || e.message),
      );
    }
  };

  const {
    register: regRecord,
    handleSubmit: submitRecord,
    reset: resetRecord,
  } = useForm<CreateMedicalRecordDTO>();

  const onSaveRecord = async (data: CreateMedicalRecordDTO) => {
    const isOffline = !isOnline;
    try {
      await coreService.createMedicalRecord({
        ...data,
        is_offline: isOffline,
      });

      if (isOffline) {
        markOfflineChange();
        await refreshOfflineCookie();
        alert('Offline: Prontuário salvo no SQLite!');
      } else {
        await loadOnlineData();
        alert('Online: Prontuário salvo no PostgreSQ!');
      }
      resetRecord();
    } catch (e: any) {
      alert(
        'Erro ao salvar prontuário: ' +
          (e.response?.data?.detail || e.message),
      );
    }
  };

  const {
    register: regAtt,
    control: controlAtt,
    handleSubmit: submitAtt,
    reset: resetAtt,
  } = useForm<CreateAttendanceDTO>({
    defaultValues: {
      consciousness_level: 15,
      medications: [],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control: controlAtt,
    name: 'medications',
  });

  const onSaveAttendance = async (data: CreateAttendanceDTO) => {
    const isOffline = !isOnline;
    const professionalId = localStorage.getItem('professional_id') || undefined;

    const payload: CreateAttendanceDTO = {
      medical_record_id: data.medical_record_id,
      professional_id: professionalId,
      patient_id: data.patient_id,
      pressure: data.pressure,
      heart_rate: Number(data.heart_rate),
      consciousness_level: Number(data.consciousness_level),
      triage_protocol: data.triage_protocol,
      notes: data.notes || '',
      is_offline: isOffline,
      medications: (data.medications || []).map((m) => ({
        medication_id: m.medication_id,
        applied_dose: m.applied_dose,
        applied_at: new Date(m.applied_at || new Date()).toISOString(),
      })),
    };

    try {
      await coreService.createAttendance(payload);

      if (isOffline) {
        markOfflineChange();
        await refreshOfflineCookie();
        alert('Offline: Atendimento salvo no SQLite!');
      } else {
        await loadOnlineData();
        alert('Online: Atendimento salvo no PostgreSQL!');
      }
      resetAtt();
    } catch (e: any) {
      alert(
        'Erro ao registrar atendimento: ' +
          (e.response?.data?.detail || e.message),
      );
    }
  };

  if (!isClientAuthenticated) {
    return (
      <div className="client-app">
        <header className="client-header">
          <h3>🚑 MedicalField App</h3>
          <span className={`badge ${isOnline ? 'bg-green' : 'bg-red'}`}>
            {isOnline ? 'Online' : 'Offline'}
          </span>
        </header>

        <div
          className="client-body"
          style={{ display: 'flex', alignItems: 'center' }}
        >
          <form
            onSubmit={submitLogin(onClientLogin)}
            className="mobile-form"
            style={{ width: '100%' }}
          >
            <h4>🔐 Login do Socorrista</h4>
            <label>Registro Profissional (CRM/COREN)</label>
            <input
              placeholder="Ex: CRM12345"
              {...regLogin('professional_registration', { required: true })}
            />

            <label>Senha</label>
            <input
              type="password"
              placeholder="******"
              {...regLogin('password', { required: true })}
            />

            <button type="submit" className="btn-submit">
              Entrar no Dispositivo
            </button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="client-app">
      <header className="client-header">
        <h3>🚑 MedicalField App</h3>
        <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
          <span className={`badge ${isOnline ? 'bg-green' : 'bg-red'}`}>
            {isOnline ? 'Online' : 'Offline'}
          </span>
          <button
            type="button"
            onClick={handleClientLogout}
            style={{
              background: '#dc2626',
              color: '#fff',
              border: 'none',
              borderRadius: 4,
              padding: '2px 6px',
              fontSize: 11,
              cursor: 'pointer',
            }}
          >
            Sair
          </button>
        </div>
      </header>

      <div className="client-body">
        {activeTab === 'attendance' && (
          <form onSubmit={submitAtt(onSaveAttendance)} className="mobile-form">
            <h4>
              Registrar Atendimento ({isOnline ? 'Online' : 'Offline SQLite'})
            </h4>

            <label>Paciente</label>
            <select {...regAtt('patient_id', { required: true })}>
              <option value="">Selecione...</option>
              {localCache.patients.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name} ({p.document})
                </option>
              ))}
            </select>

            <label>Prontuário Médico</label>
            <select {...regAtt('medical_record_id', { required: true })}>
              <option value="">Selecione...</option>
              {localCache.medicalRecords.map((mr) => (
                <option key={mr.id} value={mr.id}>
                  {mr.patient_name || `Prontuário ${mr.id.slice(0, 6)}`} (
                  {mr.blood_type})
                </option>
              ))}
            </select>

            <div className="row-2">
              <div>
                <label>Pressão</label>
                <input
                  placeholder="120/80"
                  {...regAtt('pressure', { required: true })}
                />
              </div>
              <div>
                <label>BPM (Heart Rate)</label>
                <input
                  type="number"
                  placeholder="80"
                  {...regAtt('heart_rate', {
                    required: true,
                    valueAsNumber: true,
                  })}
                />
              </div>
            </div>

            <div className="row-2">
              <div>
                <label>Glasgow (3-15)</label>
                <input
                  type="number"
                  min={3}
                  max={15}
                  {...regAtt('consciousness_level', {
                    required: true,
                    valueAsNumber: true,
                  })}
                />
              </div>
              <div>
                <label>Protocolo Triagem</label>
                <select {...regAtt('triage_protocol', { required: true })}>
                  <option value="Vermelho - Emergência">Vermelho</option>
                  <option value="Amarelo - Urgente">Amarelo</option>
                  <option value="Verde - Pouco Urgente">Verde</option>
                  <option value="Azul - Não Urgente">Azul</option>
                </select>
              </div>
            </div>

            <label>Notas</label>
            <textarea
              rows={2}
              placeholder="Observações..."
              {...regAtt('notes')}
            />

            <div className="meds-section">
              <div className="meds-header">
                <span>Medicações Aplicadas</span>
                <button
                  type="button"
                  onClick={() =>
                    append({
                      medication_id: '',
                      applied_dose: '',
                      applied_at: new Date().toISOString().slice(0, 16),
                    })
                  }
                >
                  + Adicionar
                </button>
              </div>

              {fields.map((field, index) => (
                <div key={field.id} className="med-item">
                  <select
                    {...regAtt(`medications.${index}.medication_id` as const, {
                      required: true,
                    })}
                  >
                    <option value="">Selecione o medicamento...</option>
                    {localCache.medications.map((m) => (
                      <option key={m.id} value={m.id}>
                        {m.name} ({m.standard_dosage})
                      </option>
                    ))}
                  </select>
                  <input
                    placeholder="Dose aplicada (ex: 1 ampola)"
                    {...regAtt(`medications.${index}.applied_dose` as const, {
                      required: true,
                    })}
                  />
                  <input
                    type="datetime-local"
                    {...regAtt(`medications.${index}.applied_at` as const, {
                      required: true,
                    })}
                  />
                  <button
                    type="button"
                    className="btn-remove"
                    onClick={() => remove(index)}
                  >
                    Remover
                  </button>
                </div>
              ))}
            </div>

            <button type="submit" className="btn-submit">
              Salvar Atendimento
            </button>
          </form>
        )}

        {activeTab === 'patient' && (
          <form onSubmit={submitPatient(onSavePatient)} className="mobile-form">
            <h4>Cadastrar Paciente ({isOnline ? 'Online' : 'Offline SQLite'})</h4>
            <label>Nome Completo</label>
            <input
              placeholder="Nome do paciente"
              {...regPatient('name', { required: true })}
            />

            <label>Documento</label>
            <input
              placeholder="CPF ou RG"
              {...regPatient('document', { required: true })}
            />

            <button type="submit" className="btn-submit">
              Salvar Paciente
            </button>
          </form>
        )}

        {activeTab === 'record' && (
          <form onSubmit={submitRecord(onSaveRecord)} className="mobile-form">
            <h4>Novo Prontuário ({isOnline ? 'Online' : 'Offline SQLite'})</h4>
            <label>Paciente</label>
            <select {...regRecord('patient_id', { required: true })}>
              <option value="">Selecione...</option>
              {localCache.patients.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.name} ({p.document})
                </option>
              ))}
            </select>

            <label>Tipo Sanguíneo</label>
            <input
              placeholder="O+"
              {...regRecord('blood_type', { required: true })}
            />

            <label>Alergias Conhecidas</label>
            <input
              placeholder="Nenhuma"
              {...regRecord('known_allergies', { required: true })}
            />

            <label>Condições Crônicas</label>
            <input
              placeholder="Hipertensão"
              {...regRecord('chronic_conditions', { required: true })}
            />

            <label>Contato de Emergência</label>
            <input
              placeholder="(51) 99999-9999"
              {...regRecord('emergency_contact', { required: true })}
            />

            <button type="submit" className="btn-submit">
              Salvar Prontuário
            </button>
          </form>
        )}

        {activeTab === 'sqlite_data' && (
          <div className="outbox-list">
            <h4>
              Dados Carregados ({isOnline ? 'Rotas Online' : 'SQLite / Cookie'})
            </h4>
            <div className="outbox-card">
              <strong>Pacientes ({localCache.patients.length})</strong>
              <pre>{JSON.stringify(localCache.patients, null, 2)}</pre>
            </div>
            <div className="outbox-card">
              <strong>Prontuários ({localCache.medicalRecords.length})</strong>
              <pre>{JSON.stringify(localCache.medicalRecords, null, 2)}</pre>
            </div>
            <div className="outbox-card">
              <strong>Atendimentos ({localCache.attendances.length})</strong>
              <pre>{JSON.stringify(localCache.attendances, null, 2)}</pre>
            </div>
            <div className="outbox-card">
              <strong>Medicamentos ({localCache.medications.length})</strong>
              <pre>{JSON.stringify(localCache.medications, null, 2)}</pre>
            </div>
          </div>
        )}
      </div>

      <nav className="client-bottom-nav">
        <button
          type="button"
          className={activeTab === 'attendance' ? 'active' : ''}
          onClick={() => setActiveTab('attendance')}
        >
          🩺 Atender
        </button>
        <button
          type="button"
          className={activeTab === 'patient' ? 'active' : ''}
          onClick={() => setActiveTab('patient')}
        >
          👤 Pessoa
        </button>
        <button
          type="button"
          className={activeTab === 'record' ? 'active' : ''}
          onClick={() => setActiveTab('record')}
        >
          📋 Prontuário
        </button>
        <button
          type="button"
          className={activeTab === 'sqlite_data' ? 'active' : ''}
          onClick={() => setActiveTab('sqlite_data')}
        >
          📦 Dados
        </button>
      </nav>
    </div>
  );
}