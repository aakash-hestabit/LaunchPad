import loadApp from "./loaders/app.js";
import logger from "./utils/logger.js";
const startServer = async () => {
  const app = await loadApp();
  logger.info("starting server");
  const PORT = process.env.PORT || 5000
  app.listen(PORT, () => {
        logger.info(`app is running on port ${PORT}`);
  });
};

startServer();
