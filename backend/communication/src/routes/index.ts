import { Router } from 'express';
import { generatePdf, sendEmail } from '../controller/communicationController';

const router = Router();

router.post('/generate-pdf', generatePdf);
router.post('/send-email', sendEmail);

export default router;