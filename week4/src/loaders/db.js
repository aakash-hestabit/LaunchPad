import mongoose from "mongoose";
import logger from "../utils/logger.js";

const connectDB = async () => {
  try {
    await mongoose.connect(process.env.DB_URI);
    logger.info("Database connected successfully");
  } catch (err) {
    logger.error("Database connection failed: " + err.message);
    process.exit(1);
  }
};

export default connectDB;
