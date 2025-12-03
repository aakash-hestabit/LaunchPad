module.exports = {
  apps: [
    {
      name: "job-api",
      script: "./src/index.js",
      instances: "max",
      exec_mode: "cluster",
      env: {
        NODE_ENV: "production",
        PORT: 3000,
      },
      watch: false,
      log_date_format: "YYYY-MM-DD HH:mm:ss",
      error_file: "./src/logs/app-error.log",
      out_file: "./src/logs/app-out.log",
      combine_logs: true,
    },
    {
      name: "job-worker",
      script: "./src/jobs/email.job.js",
      instances: 1,
      exec_mode: "fork",
      env: {
        NODE_ENV: "production",
      },
      log_date_format: "YYYY-MM-DD HH:mm:ss",
      error_file: "./src/logs/worker-error.log",
      out_file: "./src/logs/worker-out.log",
      combine_logs: true,
    },
  ],

  deploy: {
    production: {
      user: "SSH_USERNAME",
      host: "SSH_HOSTMACHINE",
      ref: "origin/master",
      repo: "GIT_REPOSITORY",
      path: "DESTINATION_PATH",
      "pre-deploy-local": "",
      "post-deploy":
        "npm install && pm2 reload ecosystem.config.js --env production",
      "pre-setup": "",
    },
  },
};