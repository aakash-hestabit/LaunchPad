import loadApp from "./loaders/app.js";
import logger from "./utils/logger.js";

const startServer = async () => {
  const app = await loadApp();
  logger.info("starting server");
  app.listen(3000, () => {
        console.log("app is running on port 3000");
  });
};

startServer();
