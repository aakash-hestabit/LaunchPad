import helmet from "helmet";
import rateLimit from "express-rate-limit";
import cors from "cors";
import mongoSanitize from "express-mongo-sanitize";
import xss from 'xss-clean';
import hpp from 'hpp'

export const hppPreventer = hpp()

export const xssClean = xss();

export const mongoSanitizer = mongoSanitize({
  replaceWith: "_",
});

export const securityMiddleware = helmet();

export const rateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: "Too many requests, please try again later.",
});

export const corsMiddleware = cors({
  origin: ["https://google.com"],
  methods: ["GET", "POST", "PUT", "DELETE"],
  allowedHeaders: ["Content-Type", "Authorization"],
});