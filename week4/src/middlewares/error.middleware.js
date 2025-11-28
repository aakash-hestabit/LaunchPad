import ApiError from "../utils/apiError.js";
import logger from "../utils/logger.js";

export function errorMiddleware(err, req, res, next) {
  if (!(err instanceof ApiError)) {
    err = new ApiError(
      err.message || "Internal Server Error",
      err.statusCode || 500,
      err.code || "INTERNAL_ERROR"
    );
  }

  logger.error(`code: ${err.code}, error: ${err}, timestamp: ${err.timestamp}, path: ${req.originalUrl}`)

  res.status(err.statusCode).json({
    success: false,
    message: err.message,
    code: err.code,
    timestamp: err.timestamp,
    path: req.originalUrl,
  });
}
