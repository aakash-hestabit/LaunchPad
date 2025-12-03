import { Queue, Worker } from "bullmq";
import logger from "../utils/logger.js"; 
const connection = {
  host: "127.0.0.1",
  port: 6379,
};

const emailQueue = new Queue("emailQueue", { connection });

/**
 * @param {object} data - The data for the email
 */
export async function addEmailJob(data) {
  const options = {
    attempts: 3,
    backoff: { type: "exponential", delay: 3000 },
  };

  try {
    await emailQueue.add("sendEmail", data, options);
    logger.info(`Job added to emailQueue for ${data.to}`);
  } catch (error) {
    logger.error("Error adding job to queue", { error: error.message });
    throw error;
  }
}

/**
 * @param {import('bullmq').Job} job - The job object from the queue.
 */
export async function emailProcessor(job) {
  try {
    logger.info(`Processing job ${job.id}`, { data: job.data });

    await new Promise((resolve) => setTimeout(resolve, 5000));

    logger.info(`Email successfully sent to ${job.data.to}`);

    return { status: "success", recipient: job.data.to };
  } catch (error) {
    logger.error(`Error processing job ${job.id}`, {
      error: error.message,
      data: job.data,
    });
    throw error;
  }
}

export function startEmailWorker() {
  const emailWorker = new Worker("emailQueue", emailProcessor, {
    connection,
    concurrency: 5,
  });

  emailWorker.on("completed", (job, result) => {
    logger.info(`Job ${job.id} completed`, { result });
  });

  emailWorker.on("failed", (job, err) => {
    logger.error(`Job ${job.id} failed`, {
      error: err.message,
      attemptsMade: job.attemptsMade,
    });
  });

  emailWorker.on("error", (err) => {
    logger.error("Email Worker encountered an internal error", {
      error: err.message,
    });
  });

  logger.info("Email Worker process started and listening for jobs.");
  return emailWorker;
}

export { emailQueue };
