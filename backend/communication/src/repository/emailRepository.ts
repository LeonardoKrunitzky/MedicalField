import nodemailer from 'nodemailer';
import dotenv from 'dotenv';

dotenv.config();

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
});

export const sendEmailWithAttachment = async (
  toEmail: string,
  patientName: string,
  protocol: string,
  pressure: string,
  heartRate: number,
  professionalName: string,
  pdfBuffer: Buffer
): Promise<void> => {
  await transporter.sendMail({
    from: `"MedicalField Portal" <${process.env.SMTP_USER}>`,
    to: toEmail,
    subject: `Ficha de Atendimento Médico — Paciente: ${patientName}`,
    html: `
      <div style="font-family: sans-serif; color: #1e293b;">
        <h2>🏥 MedicalField — Relatório de Atendimento</h2>
        <p>Olá,</p>
        <p>Segue em anexo o PDF contendo a ficha completa do atendimento de <strong>${patientName}</strong>.</p>
        <ul>
          <li><strong>Protocolo:</strong> ${protocol}</li>
          <li><strong>Sinais Vitais:</strong> PA ${pressure} | ${heartRate} BPM</li>
          <li><strong>Profissional:</strong> ${professionalName}</li>
        </ul>
      </div>
    `,
    attachments: [
      {
        filename: `Ficha_Atendimento_${patientName.replace(/\s+/g, '_')}.pdf`,
        content: pdfBuffer,
        contentType: 'application/pdf',
      },
    ],
  });
};