# ARCHITECTURE

## Folder Structure

    └── week4/
        ├── package.json
        └── src/
            ├── index.js
            ├── config/
            │   └── envConfig.js
            ├── controllers/
            │   └── demoRouteController.js
            ├── docs/
            │   └── ARCHITECTURE.md
            ├── loaders/
            │   ├── app.js
            │   └── db.js
            ├── routes/
            │   ├── healthRoutes.js
            │   └── index.js
            └── utils/
                └── logger.js

---

## Application Structure and Flow

### File Breakdown

- **`src/index.js`**: This is the entry point of the project, and the app is loaded here.
- **`loaders/app.js`**: This file is responsible for initializing and loading the application. It is where all the middlewares are added to the app.
- **`loaders/db.js`**: This file handles the database connection.
- **`utils/logger.js`**: Here, the global logger for the application is declared. It logs details to a log file about the progress of the application during startup.
- **`config/envConfig.js`**: This file loads environment variables from the available `.env` files.
- **`controllers/demoRouteController.js`**: This file defines a demo controller that is invoked when the `/health/demo` route is hit.
- **`routes/index.js`**: This file contains the main router that handles and manages all incoming requests.
- **`routes/healthRoutes.js`**: This file contains demo routes that help us check whether the app is running fine or not.

---

### Application Flow

1. **Environment Variables are Loaded**  
   First, the environment variables are loaded from the available `.env` files.

2. **Database Connection is Established**  
   Then, the database connection is made.

3. **Middlewares are Loaded**  
   After the database connection, all necessary middlewares are loaded into the app.

4. **App Starts on the Given Port**  
   Finally, the application starts on the specified port.
