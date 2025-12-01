import { Router } from "express";
import healthRouter from "./healthRoutes.js";
import productRouter from "./productRoutes.js";
import userRouter from './userRoutes.js'
const router = Router();

router.use("/health", healthRouter);
router.use("/products", productRouter);
router.use('/users',userRouter)

export default router;
