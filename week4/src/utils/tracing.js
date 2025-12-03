import { v4 as uuid } from 'uuid';

export function tracingMiddleware(req, res, next) {
  const requestId = req.headers['x-request-id'] || uuid();
  req.requestId = requestId;

  res.setHeader('X-Request-ID', requestId);

  next();
}

export function withTracing(logger, req) {
  return logger.child({ requestId: req.requestId });
}
