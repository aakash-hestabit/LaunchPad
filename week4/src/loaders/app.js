import express from "express";
import cookieParser from "cookie-parser";
import dbLoader from "./db.js";
import logger from "../utils/logger.js";
import loadEnvConfig from "../config/envConfig.js";
import router from "../routes/index.js";
import { errorMiddleware } from "../middlewares/error.middleware.js";
import {
  corsMiddleware,
  rateLimiter,
  securityMiddleware,
  mongoSanitizer,
  xssClean,
  hppPreventer,
} from "../middlewares/security.js";

const loadApp = async () => {
  const app = express();
  try {
    await loadEnvConfig();

    await dbLoader();

    app.use(securityMiddleware);
    app.use(xssClean);
    app.use(hppPreventer)
    app.use(mongoSanitizer);
    app.use(corsMiddleware);
    app.use(rateLimiter);
    app.use(express.urlencoded({ extended: true, limit: "16kb" }));
    app.use(express.json());
    app.use(cookieParser());
    app.use(express.static("public"));
    app.use(router);

    logger.info("Essential middlewares loaded");

    logger.info("App loaded successfully");
    app.use(errorMiddleware);
  } catch (err) {
    logger.error("Error loading app: " + err.message);
    process.exit(1);
  }
  return app;
};

export default loadApp;
