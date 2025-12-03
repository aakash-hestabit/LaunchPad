import dotenv from "dotenv";
import path from "path";
import readline from "readline";
import logger from "../utils/logger.js";

const loadEnvConfig = async () => {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  // const env = await new Promise(resolve => {
  //   rl.question('Select environment (dev, prod, local) [dev]: ', answer => {
  //     rl.close()
  //     resolve(['dev','prod','local'].includes(answer) ? answer : 'dev')
  //   })
  // })
  const env = "prod";
  const file = {
    dev: ".env.dev",
    prod: ".env.prod",
    local: ".env.local",
  }[env];

  dotenv.config({ path: path.resolve(process.cwd(), file) });
  logger.info(`Environment loaded: ${env}`);
};

export default loadEnvConfig;
