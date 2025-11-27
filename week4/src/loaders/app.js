import express from "express";
import bodyParser from "body-parser";
import cors from "cors";
import cookieParser from "cookie-parser";
import dbLoader from "./db.js";
import logger from "../utils/logger.js";
import loadEnvConfig from "../config/envConfig.js";
import router from "../routes/index.js";

const loadApp = async () => {
  const app = express();
  try {
    await loadEnvConfig();

    await dbLoader();

    app.use(cors({origin:"https://google.com"}));
    app.use(express.urlencoded({ extended: true, limit: "16kb" }));
    app.use(bodyParser.json());
    app.use(cookieParser());
    app.use(express.static("public"));
    app.use(router);

    logger.info("Essential middlewares loaded");

    logger.info("App loaded successfully");
    
  } catch (err) {
    logger.error("Error loading app: " + err.message);
    process.exit(1);
  }
  return app;
};

export default loadApp;
