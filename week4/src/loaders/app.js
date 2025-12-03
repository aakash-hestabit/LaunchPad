import express from "express";
import cookieParser from "cookie-parser";
import dbLoader from "./db.js";
import logger from "../utils/logger.js";
import loadEnvConfig from "../config/envConfig.js";
import router from "../routes/index.js";
import morgan from "morgan";
import { tracingMiddleware } from "../utils/tracing.js";
import { errorMiddleware } from "../middlewares/error.middleware.js";
import {
  corsMiddleware,
  rateLimiter,
  securityMiddleware,
  hppPreventer,
  xssSanitize,
} from "../middlewares/security.js";

const loadApp = async () => {
  const app = express();
  try {
    await loadEnvConfig();

    await dbLoader();

    app.use(securityMiddleware);
    app.use(hppPreventer);
    app.use(corsMiddleware);
    app.use(rateLimiter);
    app.use(express.urlencoded({ extended: true, limit: "16kb" }));
    app.use(express.json({ limit: "10kb" }));
    app.use(cookieParser());
    app.use(express.static("public"));
    app.use(xssSanitize);
    app.use(morgan("combined"));
    app.use(tracingMiddleware);

    app
      .get("/", (_, res) => {
        res.status(200).json("get route so far so good");
      })
      .post("/", (_, res) => {
        res.status(200).json("post route so far so good");
      });

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
