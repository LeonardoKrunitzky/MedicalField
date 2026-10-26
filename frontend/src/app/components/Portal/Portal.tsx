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
import { communicationService } from '@/app/services/communicationService';

export default function Portal() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [records, setRecords] = useState<MedicalRecord[]>([]);
  const [attendances, setAttendances] = useState<Attendance[]>([]);
  const [medications, setMedications] = useState<Medication[]>([]);
  const [selectedPatientId, setSelectedPatientId] = useState<string>('');
  const [attendanceMeds, setAttendanceMeds] = useState<
    Record<string, MedicationByAttendance[]>
  >({});

  // Estados para o envio de e-mail e geração de PDF
  const [recipientEmail, setRecipientEmail] = useState<string>('');
  const [processingId, setProcessingId] = useState<string | null>(null);

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
      return items;
    } catch {
      setAttendanceMeds((prev) => ({ ...prev, [attendanceId]: [] }));
      return [];
    }
  };

  // Monta o objeto consolidado cruzando Paciente + Prontuário + Atendimento + Medicações
  const buildReportPayload = async (att: Attendance) => {
    let medsList = attendanceMeds[att.id];
    if (!medsList) {
      medsList = await handleLoadAttendanceMeds(att.id);
    }

    const patient = patients.find(
      (p) => p.id === att.patient_id || p.name === att.patient_name
    );
    const record = records.find(
      (r) =>
        r.id === att.medical_record_id ||
        r.patient_id === att.patient_id ||
        r.patient_name === att.patient_name
    );

    return {
      attendance_id: att.id,
      patient_name: att.patient_name || patient?.name || 'Paciente',
      patient_document: patient?.document,
      professional_name: att.professional_name,
      pressure: att.pressure,
      heart_rate: att.heart_rate,
      consciousness_level: att.consciousness_level,
      triage_protocol: att.triage_protocol,
      notes: att.notes,
      created_at: att.created_at,
      blood_type: record?.blood_type,
      known_allergies: record?.known_allergies,
      chronic_conditions: record?.chronic_conditions,
      emergency_contact: record?.emergency_contact,
      medications: medsList.map((m) => ({
        name: m.name,
        applied_dose: m.applied_dose,
        standard_dosage: m.standard_dosage,
      })),
    };
  };

  // Passo 16: Baixar PDF da Ficha de Atendimento
  const handleDownloadPdf = async (att: Attendance) => {
    try {
      setProcessingId(att.id);
      const payload = await buildReportPayload(att);
      await communicationService.downloadAttendancePdf(payload);
    } catch (error) {
      console.error('Erro ao baixar PDF:', error);
      alert('Erro ao gerar o PDF de atendimento.');
    } finally {
      setProcessingId(null);
    }
  };

  // Passo 17: Enviar PDF por E-mail
  const handleSendEmail = async (att: Attendance) => {
    const emailToUse =
      recipientEmail.trim() ||
      window.prompt('Digite o e-mail de destino para enviar a ficha em PDF:') ||
      '';

    if (!emailToUse.trim()) return;

    try {
      setProcessingId(att.id);
      const payload = await buildReportPayload(att);
      await communicationService.sendAttendanceEmail(emailToUse.trim(), payload);
      alert(`Ficha em PDF enviada com sucesso para ${emailToUse}!`);
    } catch (error) {
      console.error('Erro ao enviar e-mail:', error);
      alert('Falha ao enviar o e-mail. Verifique o serviço de comunicação.');
    } finally {
      setProcessingId(null);
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
          <div className="section-controls">
            <input
              type="email"
              className="email-input"
              placeholder="E-mail destino (ex: paciente@gmail.com)"
              value={recipientEmail}
              onChange={(e) => setRecipientEmail(e.target.value)}
            />
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
              <th>Ações (PDF / E-mail)</th>
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
                        {attendanceMeds[att.id].map((m, i) => (
                          <li key={i}>
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
                <td>
                  <div className="action-buttons">
                    <button
                      type="button"
                      className="btn-pdf"
                      disabled={processingId === att.id}
                      onClick={() => handleDownloadPdf(att)}
                    >
                      📄 PDF
                    </button>
                    <button
                      type="button"
                      className="btn-email"
                      disabled={processingId === att.id}
                      onClick={() => handleSendEmail(att)}
                    >
                      {processingId === att.id ? '⏳...' : '✉️ E-mail'}
                    </button>
                  </div>
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