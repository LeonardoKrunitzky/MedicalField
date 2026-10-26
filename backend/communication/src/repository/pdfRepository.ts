import PDFDocument from 'pdfkit';
import type { AttendanceReportPayload } from '../types/payload.ts';

export const buildAttendancePdfBuffer = (data: AttendanceReportPayload): Promise<Buffer> => {
  return new Promise((resolve, reject) => {
    const doc = new PDFDocument({ margin: 50, size: 'A4' });
    const buffers: Buffer[] = [];

    doc.on('data', (chunk) => buffers.push(chunk));
    doc.on('end', () => resolve(Buffer.concat(buffers)));
    doc.on('error', (err) => reject(err));

    doc.fontSize(20).fillColor('#0f172a').text('MedicalField — Ficha de Atendimento', { align: 'center' });
    doc.moveDown(0.3);
    doc.fontSize(10).fillColor('#64748b').text(`ID do Atendimento: ${data.attendance_id}`, { align: 'center' });

    doc.moveDown(1);
    doc.moveTo(50, doc.y).lineTo(545, doc.y).strokeColor('#cbd5e1').stroke();
    doc.moveDown(1);

    doc.fontSize(14).fillColor('#1e293b').text('1. Identificação e Prontuário');
    doc.moveDown(0.5);
    doc.fontSize(11).fillColor('#334155');
    doc.text(`Paciente: ${data.patient_name || 'Não informado'}`);
    if (data.patient_document) doc.text(`Documento (CPF/RG): ${data.patient_document}`);
    if (data.blood_type) doc.text(`Tipo Sanguíneo: ${data.blood_type}`);

    doc.moveDown(1);
    doc.fontSize(14).fillColor('#1e293b').text('2. Dados Clínicos e Triagem');
    doc.moveDown(0.5);
    doc.fontSize(11).fillColor('#334155');
    doc.text(`Profissional Responsável: ${data.professional_name}`);
    doc.text(`Protocolo: ${data.triage_protocol}`);
    doc.text(`Sinais Vitais: PA ${data.pressure} | ${data.heart_rate} BPM`);
    doc.text(`Glasgow: ${data.consciousness_level}`);

    doc.moveDown(1);
    doc.fontSize(14).fillColor('#1e293b').text('3. Medicações Aplicadas');
    doc.moveDown(0.5);
    doc.fontSize(11).fillColor('#334155');

    if (data.medications && data.medications.length > 0) {
      data.medications.forEach((med, idx) => {
        doc.text(`${idx + 1}. ${med.name} — Dose: ${med.applied_dose}`);
      });
    } else {
      doc.text('Nenhuma medicação registrada.');
    }

    doc.end();
  });
};