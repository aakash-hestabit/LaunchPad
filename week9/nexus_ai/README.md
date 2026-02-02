# NEXUS AI

#### Features- 
- Multi-agent orchestration
- Parallel task execution
- Memory-based reasoning
- Self-correction via validation feedback
- Autonomous replanning

---

## Project Structure
```
nexus-ai/
│
├── agents/
│ ├── orchestrator.py
│ ├── planner.py
│ ├── researcher.py
│ ├── coder.py
│ ├── analyst.py
│ ├── critic.py
│ ├── optimizer.py
│ ├── validator.py
│ └── reporter.py
│
├── main.py
├── config.py
├── logs/
│
├── ARCHITECTURE.md
├── FINAL-REPORT.md
└── README.md
```

---
## Running the System (Local)
```bash
pip install -r requirements.txt
```
- Run the main file
```bash
python -m main
```

## Running the System (Docker)


### Build & Start

```bash
docker compose up --build
```
after the build completes and for running the image in future
```bash
docker compose run nexus-ai
```

#### How It Works

User provides a task.

Planner creates an execution plan (DAG of agents).

Orchestrator executes agents in parallel levels.

Validator checks output quality.

If validation fails -> system replans automatically.

If validation succeeds -> Reporter generates final output.

#### NOTES 
Logs are stored in the logs/ folder.

The system supports autonomous retries and replanning.

API keys should be provided using a .env file.