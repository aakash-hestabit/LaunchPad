import { addEmailJob, startEmailWorker } from "../jobs/email.job.js";
import logger from "../utils/logger.js";
import { withTracing } from "../utils/tracing.js";

export async function sendEmailHandler(req, res, next) {
  try {
    const log = withTracing(logger, req);

    const { to, subject, message } = req.body;

    if (!to) return res.status(400).json({ error: "Missing email recipient" });

    await addEmailJob({ to, subject, message });

    log.info(`Email job queued for ${to}`);

    startEmailWorker();

    res.json({ status: "queued", requestId: req.requestId });
  } catch (e) {
    next(e);
  }
}
