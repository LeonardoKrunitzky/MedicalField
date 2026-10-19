'use client';

import React, { useState, useEffect } from 'react';
import { useForm, useFieldArray } from 'react-hook-form';
import { useNetwork } from '../../../context/NetworkContext';
import { coreService } from '../../services/coreService';
import {
  CreatePatientDTO,
  CreateMedicalRecordDTO,
  CreateAttendanceDTO,
} from '../../types';
import './Client.css';

type TabType = 'attendance' | 'patient' | 'record' | 'outbox';

export default function Client() {
  const [activeTab, setActiveTab] = useState<TabType>('attendance');
  const { isOnline, localCache, outboxQueue, enqueueOperation, handleManualSync } =
    useNetwork();

  // 1. Formulário de Paciente
  const {
    register: regPatient,
    handleSubmit: submitPatient,
    reset: resetPatient,
  } = useForm<CreatePatientDTO>();

  const onSavePatient = async (data: CreatePatientDTO) => {
    if (isOnline) {
      try {
        await coreService.createPatient(data);
        alert('Paciente salvo!');
        await handleManualSync();
      } catch (e: any) {
        alert('Erro ao cadastrar paciente: ' + (e.response?.data?.detail || e.message));
      }
    } else {
      enqueueOperation('PATIENT', data);
      alert('Offline: Paciente adicionado na fila local (Outbox)!');
    }
    resetPatient();
  };

  // 2. Formulário de Prontuário
  const {
    register: regRecord,
    handleSubmit: submitRecord,
    reset: resetRecord,
  } = useForm<CreateMedicalRecordDTO>();

  const onSaveRecord = async (data: CreateMedicalRecordDTO) => {
    if (isOnline) {
      try {
        await coreService.createMedicalRecord(data);
        alert('Prontuário salvo!');
        await handleManualSync();
      } catch (e: any) {
        alert('Erro ao salvar prontuário: ' + (e.response?.data?.detail || e.message));
      }
    } else {
      enqueueOperation('MEDICAL_RECORD', data);
      alert('Offline: Prontuário adicionado na fila local (Outbox)!');
    }
    resetRecord();
  };

  // 3. Formulário de Atendimento
  const {
    register: regAtt,
    control: controlAtt,
    handleSubmit: submitAtt,
    reset: resetAtt,
    setValue: setAttValue,
  } = useForm<CreateAttendanceDTO>({
    defaultValues: {
      professional_id: '',
      consciousness_level: 15,
      medications: [],
    },
  });

  useEffect(() => {
    const profId = localStorage.getItem('professional_id');
    if (profId) {
      setAttValue('professional_id', profId);
    }
  }, [setAttValue]);

  const { fields, append, remove } = useFieldArray({
    control: controlAtt,
    name: 'medications',
  });

  const onSaveAttendance = async (data: CreateAttendanceDTO) => {
    const payload: CreateAttendanceDTO = {
      medical_record_id: data.medical_record_id,
      professional_id: data.professional_id,
      patient_id: data.patient_id,
      pressure: data.pressure,
      heart_rate: Number(data.heart_rate),
      consciousness_level: Number(data.consciousness_level),
      triage_protocol: data.triage_protocol,
      notes: data.notes || '',
      medications: (data.medications || []).map((m) => ({
        medication_id: m.medication_id,
        applied_dose: m.applied_dose,
        applied_at: new Date(m.applied_at || new Date()).toISOString(),
      })),
    };

    if (isOnline) {
      try {
        await coreService.createAttendance(payload);
        alert('Atendimento registrado!');
      } catch (e: any) {
        alert('Erro ao registrar atendimento: ' + (e.response?.data?.detail || e.message));
      }
    } else {
      enqueueOperation('ATTENDANCE', payload);
      alert('Offline: Atendimento salvo na fila Outbox!');
    }
    resetAtt();
  };

  return (
    <div className="client-app">
      <header className="client-header">
        <h3>🚑 MedicalField App</h3>
        <span className={`badge ${isOnline ? 'bg-green' : 'bg-red'}`}>
          {isOnline ? 'Online' : 'Offline'}
        </span>
      </header>

      <div className="client-body">
        {activeTab === 'attendance' && (
          <form onSubmit={submitAtt(onSaveAttendance)} className="mobile-form">
            <h4>Registrar Atendimento</h4>

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
                  {mr.patient_name || `ID: ${mr.id.slice(0, 6)}`} ({mr.blood_type})
                </option>
              ))}
            </select>

            <label>ID do Profissional (UUID)</label>
            <input
              placeholder="UUID do profissional"
              {...regAtt('professional_id', { required: true })}
            />

            <div className="row-2">
              <div>
                <label>Pressão</label>
                <input placeholder="120/80" {...regAtt('pressure', { required: true })} />
              </div>
              <div>
                <label>BPM (Heart Rate)</label>
                <input
                  type="number"
                  placeholder="80"
                  {...regAtt('heart_rate', { required: true, valueAsNumber: true })}
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
                  {...regAtt('consciousness_level', { required: true, valueAsNumber: true })}
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
            <textarea rows={2} placeholder="Observações..." {...regAtt('notes')} />

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
                  <button type="button" className="btn-remove" onClick={() => remove(index)}>
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
            <h4>Cadastrar Paciente</h4>
            <label>Nome Completo</label>
            <input placeholder="Nome do paciente" {...regPatient('name', { required: true })} />

            <label>Documento</label>
            <input placeholder="CPF ou RG" {...regPatient('document', { required: true })} />

            <button type="submit" className="btn-submit">
              Salvar Paciente
            </button>
          </form>
        )}

        {activeTab === 'record' && (
          <form onSubmit={submitRecord(onSaveRecord)} className="mobile-form">
            <h4>Novo Prontuário</h4>
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
            <input placeholder="O+" {...regRecord('blood_type', { required: true })} />

            <label>Alergias Conhecidas</label>
            <input placeholder="Nenhuma" {...regRecord('known_allergies', { required: true })} />

            <label>Condições Crônicas</label>
            <input placeholder="Hipertensão" {...regRecord('chronic_conditions', { required: true })} />

            <label>Contato de Emergência</label>
            <input placeholder="(51) 99999-9999" {...regRecord('emergency_contact', { required: true })} />

            <button type="submit" className="btn-submit">
              Salvar Prontuário
            </button>
          </form>
        )}

        {activeTab === 'outbox' && (
          <div className="outbox-list">
            <h4>Fila Outbox ({outboxQueue.length})</h4>
            {outboxQueue.length === 0 ? (
              <p className="empty-msg">Nenhum registro pendente de sincronização.</p>
            ) : (
              outboxQueue.map((item) => (
                <div key={item.tempId} className="outbox-card">
                  <strong>{item.type}</strong>
                  <span>{new Date(item.createdAt).toLocaleTimeString()}</span>
                  <pre>{JSON.stringify(item.payload, null, 2)}</pre>
                </div>
              ))
            )}
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
          className={activeTab === 'outbox' ? 'active' : ''}
          onClick={() => setActiveTab('outbox')}
        >
          📦 Fila ({outboxQueue.length})
        </button>
      </nav>
    </div>
  );
}