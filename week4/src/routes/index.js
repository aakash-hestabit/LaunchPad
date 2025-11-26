import { Router } from "express";
import healthRouter from './healthRoutes.js'

const router = Router();

router.use('/health',healthRouter);

export default router