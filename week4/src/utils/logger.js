import winston from "winston";
import path from "path";
import { format, createLogger } from "winston";
const { combine, printf, timestamp } = format;
const logFilePath = path.join(process.cwd(), "src", "logs", "app.log");

const logger = createLogger({
  levels: winston.config.npm.levels,
  format: combine(
    timestamp({ format: "YYYY-MM-DD HH:mm:ss" }),
    printf(
      ({ timestamp, level, message }) => `${timestamp} ${level} : ${message}`
    )
  ),
  transports: [
    new winston.transports.Console(),
    new winston.transports.File({ filename: logFilePath }),
  ],
});

export default logger;
