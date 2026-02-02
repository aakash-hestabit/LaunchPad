# NEXUS AI — System Architecture


##  Flow
```
User Query
    |
Planner -> Execution Plan (DAG)
    |
Orchestrator (Control Engine)
    |
Parallel Agent Execution (DAG Levels)
    |
Validator (Quality Gate)
    |
[ FAIL -> Replan ] OR [ PASS -> Reporter ]
```
---


| Layer | Responsibility |
|------|----------------|
Entry Layer | `main.py` handles user input and system start |
Planning Layer | Planner decomposes tasks into steps and dependencies |
Control Layer | Orchestrator manages execution, retries, validation, and replanning |
Agent Layer | Specialized agents perform domain tasks |
Memory Layer | Memory manager provides contextual recall |
Logging Layer | System logs execution traces and failures |

---

##  Core Components

### 1. Planner
- Converts user goals into structured execution steps
- Produces a Directed Acyclic Graph (DAG)
- Identifies dependencies for parallel execution

---

### 2. Orchestrator 

The orchestrator is the brain of the system. It implements:

| Mechanism | Purpose |
|-----------|--------|
Level-based scheduling | Executes independent agents in parallel |
Failure-aware retries | Retries agents using feedback from previous errors |
Goal alignment | Passes original user goal to all agents |
Memory injection | Provides contextual knowledge to agents |
Validation control gate | Stops execution on quality failure |
Autonomous replanning | Generates improved plans using validator feedback |

---

### 3. Agents

Each agent has a specialized function:

| Agent | Function |
|------|-----------|
Researcher | Information gathering |
Analyst | Data analysis |
Coder | Technical solution development |
Critic | Quality review |
Optimizer | Performance enhancement |
Validator | Final quality assurance |
Reporter | Final structured output |

Agents operate under orchestrator control and never independently decide the workflow.

---

## Execution

###  DAG-Based Parallel Execution
- The planner outputs steps with dependencies
- The orchestrator computes execution levels
- Agents in the same level run concurrently

---

### Failure-Aware Retry System
When an agent fails:
- The error is captured
- The agent is retried with failure context
- This enables self-correction

---

###  Memory
- Past interactions are stored
- Relevant memory is injected into agent prompts
- Supports contextual continuity

---

### Validation-Driven Replanning
If Validator outputs failure:
1. Execution halts immediately
2. Output directory is cleared
3. Planner regenerates improved plan using feedback
4. Execution resumes

This forms a **closed feedback loop**.

---

## Autonomous Control Loop

The system continuously evaluates its own output:

Execute -> Evaluate -> Improve -> Re-execute

yaml
Copy code

This enables:
- Self-reflection
- Self-improvement
- Goal-oriented adaptation

---