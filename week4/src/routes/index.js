import { Router } from "express";
import healthRouter from "./healthRoutes.js";
import productRouter from "./productRoutes.js";

const router = Router();

router.use("/health", healthRouter);
router.use("/products", productRouter);

export default router;
