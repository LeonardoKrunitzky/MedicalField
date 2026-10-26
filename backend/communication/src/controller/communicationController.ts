import type { Request, Response } from 'express';
import { buildAttendancePdfBuffer } from '../repository/pdfRepository';
import { sendEmailWithAttachment } from '../repository/emailRepository';
import type { AttendanceReportPayload } from '../types/payload.ts';
import axios from 'axios';

// Função auxiliar para enviar o log sem bloquear o fluxo principal (Fire-and-forget)
const dispatchTrace = (req: Request, statusCode: number, startTime: number): void => {
  const processingTimeMs = Date.now() - startTime;
  
  // Extração do IP (suporte a proxy)
  const forwardedFor = req.headers['x-forwarded-for'] as string;
  const clientIp = forwardedFor 
    ? forwardedFor.split(',')[0].trim() 
    : req.socket.remoteAddress || 'unknown';

  // Extração do ID do profissional via token JWT
  let professionalId: string | null = null;
  const authHeader = req.headers.authorization;
  if (authHeader && authHeader.startsWith('Bearer ')) {
    try {
      const tokenPayload = authHeader.split(' ')[1].split('.')[1];
      const decoded = JSON.parse(Buffer.from(tokenPayload, 'base64').toString());
      professionalId = decoded.sub || null;
    } catch (e) {
      // Ignora silenciosamente se o token for inválido
    }
  }

  const logData = {
    client_ip: clientIp,
    professional_id: professionalId,
    http_method: req.method,
    route: req.originalUrl || req.url,
    status_code: statusCode,
    processing_time_ms: processingTimeMs,
    created_at: new Date().toISOString(),
  };

  const tracingUrl = process.env.TRACING_URL || '';

  axios.post(tracingUrl, logData, { timeout: 3000 }).catch((error) => {
    const errMsg = error instanceof Error ? error.message : 'Erro desconhecido';
    console.error(`Erro ao enviar log para Tracing (Go): ${errMsg}`);
  });
};

export const generatePdf = async (req: Request, res: Response): Promise<void> => {
  const startTime = Date.now();
  try {
    const reportData = req.body as AttendanceReportPayload;
    const pdfBuffer = await buildAttendancePdfBuffer(reportData);

    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader(
      'Content-Disposition',
      `attachment; filename=atendimento-${reportData.attendance_id}.pdf`
    );
    res.send(pdfBuffer);
    
    dispatchTrace(req, 200, startTime);
  } catch (error) {
    console.error('Erro ao gerar PDF:', error);
    res.status(500).json({ message: 'Erro ao gerar arquivo PDF.' });
    
  
    dispatchTrace(req, 500, startTime);
  }
};

export const sendEmail = async (req: Request, res: Response): Promise<void> => {
  const startTime = Date.now();
  try {
    const { toEmail, reportData }: { toEmail: string; reportData: AttendanceReportPayload } = req.body;

    if (!toEmail) {
      res.status(400).json({ message: 'O e-mail de destino (toEmail) é obrigatório.' });
      dispatchTrace(req, 400, startTime);
      return;
    }

    const pdfBuffer = await buildAttendancePdfBuffer(reportData);

    await sendEmailWithAttachment(
      toEmail,
      reportData.patient_name,
      reportData.triage_protocol,
      reportData.pressure,
      reportData.heart_rate,
      reportData.professional_name,
      pdfBuffer
    );

    res.status(200).json({ message: 'E-mail com PDF enviado com sucesso!' });
    dispatchTrace(req, 200, startTime);
  } catch (error) {
    console.error('Erro ao enviar e-mail:', error);
    res.status(500).json({ message: 'Falha ao enviar o e-mail.' });
    dispatchTrace(req, 500, startTime);
  }
};