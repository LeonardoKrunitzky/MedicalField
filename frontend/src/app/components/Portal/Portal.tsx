'use client';

import React, { useEffect, useState } from 'react';
import { coreService } from '../../services/coreService';
import type {
  Patient,
  MedicalRecord,
  Attendance,
  Medication,
  MedicationByAttendance,
} from '../../types';
import './Portal.css';

export default function Portal() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [records, setRecords] = useState<MedicalRecord[]>([]);
  const [attendances, setAttendances] = useState<Attendance[]>([]);
  const [medications, setMedications] = useState<Medication[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState<string>('');
  const [attendanceMeds, setAttendanceMeds] = useState<
    Record<string, MedicationByAttendance[]>
  >({});

  const loadAllData = async () => {
    try {
      const [pts, recs, atts, meds] = await Promise.all([
        coreService.getPatients(),
        coreService.getMedicalRecords(),
        coreService.getAttendances(),
        coreService.getMedications(),
      ]);
      setPatients(pts);
      setRecords(recs);
      setAttendances(atts);
      setMedications(meds);
    } catch (err) {
      console.error('Erro ao carregar dados do Portal:', err);
    }
  };

  useEffect(() => {
    loadAllData();
  }, []);

  const handleFilterByPatient = async (patientId: string) => {
    setSelectedPatientId(patientId);
    if (!patientId) {
      const all = await coreService.getAttendances();
      setAttendances(all);
      return;
    }
    try {
      const filtered = await coreService.getAttendancesByPatient(patientId);
      setAttendances(filtered);
    } catch {
      setAttendances([]);
    }
  };

  const handleLoadAttendanceMeds = async (attendanceId: string) => {
    try {
      const items = await coreService.getMedicationsByAttendance(attendanceId);
      setAttendanceMeds((prev) => ({ ...prev, [attendanceId]: items }));
    } catch {
      setAttendanceMeds((prev) => ({ ...prev, [attendanceId]: [] }));
    }
  };

  return (
    <div className="portal-container">
      <div className="portal-header">
        <div>
          <h1>🏥 MedicalField — Portal Central (Nuvem)</h1>
          <p>
            Gestão de pacientes, prontuários, medicamentos e atendimentos
            sincronizados
          </p>
        </div>
        <button type="button" className="btn-refresh" onClick={loadAllData}>
          🔄 Atualizar Dados
        </button>
      </div>

      <div className="portal-stats">
        <div className="stat-card">
          <span>Pacientes Cadastrados</span>
          <strong>{patients.length}</strong>
        </div>
        <div className="stat-card">
          <span>Prontuários Médicos</span>
          <strong>{records.length}</strong>
        </div>
        <div className="stat-card">
          <span>Atendimentos na Nuvem</span>
          <strong>{attendances.length}</strong>
        </div>
        <div className="stat-card">
          <span>Catálogo de Medicamentos</span>
          <strong>{medications.length}</strong>
        </div>
      </div>

      {}
      <section className="portal-section">
        <div className="section-header">
          <h2>Pacientes Cadastrados</h2>
        </div>
        <table className="portal-table">
          <thead>
            <tr>
              <th>Nome</th>
              <th>Documento (CPF/RG)</th>
              <th>ID (UUID)</th>
            </tr>
          </thead>
          <tbody>
            {patients.map((p) => (
              <tr key={p.id}>
                <td>
                  <strong>{p.name}</strong>
                </td>
                <td>{p.document}</td>
                <td className="uuid-cell">{p.id}</td>
              </tr>
            ))}
            {patients.length === 0 && (
              <tr>
                <td colSpan={3} style={{ textAlign: 'center' }}>
                  Nenhum paciente sincronizado.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </section>

      <section className="portal-section">
        <div className="section-header">
          <h2>Atendimentos Registrados</h2>
          <select
            value={selectedPatientId}
            onChange={(e) => handleFilterByPatient(e.target.value)}
          >
            <option value="">Todos os Pacientes</option>
            {patients.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name} ({p.document})
              </option>
            ))}
          </select>
        </div>

        <table className="portal-table">
          <thead>
            <tr>
              <th>Paciente</th>
              <th>Profissional</th>
              <th>Sinais Vitais</th>
              <th>Glasgow</th>
              <th>Protocolo</th>
              <th>Notas</th>
              <th>Medicações</th>
            </tr>
          </thead>
          <tbody>
            {attendances.map((att) => (
              <tr key={att.id}>
                <td>{att.patient_name}</td>
                <td>{att.professional_name}</td>
                <td>
                  PA: {att.pressure} | {att.heart_rate} BPM
                </td>
                <td>{att.consciousness_level}</td>
                <td>
                  <span className="protocol-tag">{att.triage_protocol}</span>
                </td>
                <td>{att.notes}</td>
                <td>
                  {attendanceMeds[att.id] ? (
                    attendanceMeds[att.id].length > 0 ? (
                      <ul>
                        {attendanceMeds[att.id].map((m) => (
                          <li key={m.id}>
                            {m.name} ({m.applied_dose})
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <span>Nenhuma</span>
                    )
                  ) : (
                    <button
                      type="button"
                      className="btn-small"
                      onClick={() => handleLoadAttendanceMeds(att.id)}
                    >
                      Ver Medicações
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <div className="portal-grid-2">
        <section className="portal-section">
          <h2>Prontuários Médicos</h2>
          <table className="portal-table">
            <thead>
              <tr>
                <th>Paciente</th>
                <th>Sangue</th>
                <th>Alergias</th>
                <th>Crônicas</th>
                <th>Emergência</th>
              </tr>
            </thead>
            <tbody>
              {records.map((r) => (
                <tr key={r.id}>
                  <td>{r.patient_name}</td>
                  <td>
                    <strong>{r.blood_type}</strong>
                  </td>
                  <td>{r.known_allergies}</td>
                  <td>{r.chronic_conditions}</td>
                  <td>{r.emergency_contact}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="portal-section">
          <h2>Catálogo de Medicamentos</h2>
          <table className="portal-table">
            <thead>
              <tr>
                <th>Nome</th>
                <th>Dosagem Padrão</th>
                <th>UUID</th>
              </tr>
            </thead>
            <tbody>
              {medications.map((m) => (
                <tr key={m.id}>
                  <td>
                    <strong>{m.name}</strong>
                  </td>
                  <td>{m.standard_dosage}</td>
                  <td className="uuid-cell">{m.id}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </div>
    </div>
  );
}