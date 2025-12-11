import helmet from "helmet";
import rateLimit from "express-rate-limit";
import cors from "cors";
import hpp from "hpp";
import { xss } from "express-xss-sanitizer";

export const hppPreventer = hpp();

export const xssSanitize = xss();

export const securityMiddleware = helmet();

export const rateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, //15 minutes time window
  max: 10,
  message: "Too many requests, please try again later.",
});

export const corsMiddleware = cors({
  origin: ["http://localhost:3000", "http://127.0.0.1:5501"],
  methods: ["GET", "POST", "PUT", "DELETE"],
  allowedHeaders: ["Content-Type", "Authorization"],
});
