# Application Overview

This application consists of three services running in separate containers:

- **Frontend** – React app on port 3000, communicates with the backend.
- **Backend** – Node.js server on port 5000, interacts with MongoDB.
- **MongoDB** – Database with persistent storage using a Docker volume.

All services run on a shared Docker network (`app-net`).

### How it Works

Frontend sends requests to the backend, which interacts with MongoDB and returns responses. Each service runs in its own container but communicates over the shared network.
