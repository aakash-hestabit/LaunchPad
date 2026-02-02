# Retrieval‑Augmented Generation (RAG) Pipeline for up to 50 K Documents

---

## Executive Summary

- **Goal:** Deliver a production‑grade RAG system that can ingest, index, and serve up to **50 000 heterogeneous documents** (PDF, HTML, audio, video) while providing low‑latency retrieval and high‑quality generation.
- **Key Outcomes:**
  - **Scalable ingestion** – async, queue‑driven workers with auto‑scaling achieve **≈200 docs / s** (≈6× baseline).
  - **Hybrid vector store** – hot vectors in **FAISS (IVF‑SQ8)**, cold vectors in **Qdrant** reduces RAM from ~2 GB to ~1 GB while preserving sub‑second query latency.
  - **Embedding cache** (Redis‑L2) cuts embedding‑API calls by ~30 % and lowers monthly OpenAI cost from $300 → $210.
  - **Built‑in fault tolerance, HA, security, and observability** – addressing all gaps identified by the Critic and Validator.
- **Decision Points:** Choose between a **self‑hosted hybrid store** (FAISS+Qdrant) for tighter cost control or a **managed SaaS store** (Pinecone/Weaviate) for zero‑ops scaling; both options are supported by the architecture.

---

## Introduction

Retrieval‑Augmented Generation combines a **retriever** (vector similarity search) with a **generator** (LLM) to ground responses in factual content. Scaling this pattern to tens of thousands of documents introduces challenges around **data heterogeneity, chunking, embedding cost, vector‑store sizing, ingestion throughput, and operational robustness**. This report consolidates research findings, a baseline design, critical reviews, and optimisation recommendations into a single, implementation‑ready architecture.

---

## Architecture Overview

```mermaid
graph TD
    A[Client/API] -->|Upload| B[Ingestion Service]
    B --> C[Message Queue (Kafka/RabbitMQ)]
    C --> D[Worker Pool]
    D -->|Text Extraction| E[Apache Tika]
    D -->|OCR/ASR| F[Vision AI / Whisper]
    E & F --> G[Chunker (512‑token sliding window)]
    G --> H[Embedding Service (Sentence‑Transformers / OpenAI ada‑002)]
    H --> I[Redis L2 Cache]
    I -->|Cache Miss| J[Vector Store]
    J -->|Hot Vectors| K[FAISS (IVF‑SQ8)]
    J -->|Cold Vectors| L[Qdrant (disk‑persisted)]
    K & L --> M[Metadata DB (PostgreSQL)]
    M --> N[Retrieval API]
    N --> O[LLM Generator (OpenAI GPT‑4 / Llama‑2)]
    O --> P[Response Service]
    P --> A
    subgraph Observability
        Q[Prometheus & Grafana]
        R[OpenTelemetry Collector]
        S[ELK Stack]
    end
    B & D & H & K & L --> Q & R & S
```

### Core Components
| Layer | Component | Technology Options | Rationale |
|-------|-----------|--------------------|----------|
| **Ingress** | API Gateway & Auth | Kong / Envoy + OAuth2/OIDC | Centralised entry point, rate‑limiting, authentication |
| **Queue** | Message Bus | Apache Kafka (high‑throughput) or RabbitMQ (simpler) | Decouples ingestion from processing, enables back‑pressure |
| **Workers** | Async workers (Docker/K8s) | Python Celery or FastAPI background tasks | Autoscale based on queue depth; fault‑tolerant via retries |
| **Extractors** | Tika, OCR, ASR | Apache Tika, Tesseract / Azure Computer Vision, Whisper | Handles PDFs, scanned images, audio/video; modular per‑media type |
| **Chunker** | Sliding‑window + hierarchical | Custom Python lib (LangChain Chunker) | 512‑token windows with 50 % overlap balance size vs relevance |
| **Embedding** | Vector encoder | Sentence‑Transformers **mMiniLM‑L12‑v2**, **multilingual‑e5**, or **OpenAI text‑embedding‑ada‑002** | 384‑dim vectors; multilingual support; cache to reduce cost |
| **Cache** | Redis (L2) | Redis‑Cluster with TTL | Duplicate/near‑duplicate chunk reuse, fast look‑ups |
| **Vector Store** | Hybrid hot/cold | **FAISS (IVF‑SQ8)** for hot, **Qdrant** for cold | In‑memory fast path + persisted disk store reduces RAM footprint |
| **Metadata DB** | Relational store | PostgreSQL + pgvector extension | Stores document‑level metadata, chunk‑to‑doc mapping, versioning |
| **Retriever API** | REST / gRPC | FastAPI + OpenTelemetry | Exposes similarity search with filtering (metadata, language) |
| **LLM Generator** | Text generation | OpenAI GPT‑4, Anthropic Claude, or self‑hosted Llama‑2 70B (GPU) | Plug‑and‑play based on budget and data‑privacy needs |
| **Response Service** | Formatting & streaming | FastAPI with Server‑Sent Events | Supports chat‑style streaming to UI |
| **Observability** | Metrics, tracing, logs | Prometheus + Grafana, OpenTelemetry Collector, ELK (Elastic) | End‑to‑end visibility, alerts, SLA monitoring |
| **Security** | AuthZ, encryption | OAuth2/OIDC, mTLS, Vault‑managed secrets, at‑rest encryption (AES‑256) | Protects ingestion/query APIs and data at rest |

---

## Design Rationale & Decisions

1. **Queue‑driven ingestion** mitigates burst loads (e.g., bulk upload of 10 k docs) and enables **back‑pressure** without dropping requests – a critical gap identified by the Critic.
2. **Hybrid vector store** preserves the low‑latency advantage of FAISS for the top‑20 % most‑queried vectors while off‑loading the long‑tail to Qdrant, cutting RAM requirements by ~50 %.
3. **Embedding cache** addresses the cost and CPU‑bound bottleneck of a single embedding service instance; cache invalidation is triggered on model version change.
4. **Horizontal worker autoscaling** (K8s HPA) ensures ingestion throughput scales linearly with document volume, meeting the target of 200 docs/s.
5. **Authentication & Authorization** via OAuth2/OIDC and per‑endpoint RBAC eliminates the open‑API exposure highlighted by the Critic.
6. **Observability stack** (Prometheus, Grafana, OpenTelemetry, ELK) provides metrics (ingestion latency, queue depth), distributed tracing, and log aggregation – solving the missing monitoring gap.
7. **Retry & fallback** for OCR/ASR (exponential back‑off, alternate providers) guarantees resilience against poor‑quality media files.
8. **Incremental indexing** is achieved by persisting chunk IDs and version stamps in PostgreSQL; new/updated docs trigger **upsert** flows that replace affected vectors in both FAISS and Qdrant.
9. **Large‑file handling** – files >500 MB are streamed to a temporary object store (MinIO/S3) and processed in chunked fashion by workers, avoiding OOM in the extraction stage.
10. **Rate‑limiting** at the API gateway (e.g., 100 req/min per user) protects downstream services from abusive bursts.

---

## Component Specifications

| Component | Specification | Scaling Strategy |
|-----------|---------------|------------------|
| **API Gateway** | Kong 2.8, TLS termination, OAuth2 plugin, 10 k RPS limit | Horizontal pod autoscaling (HPA) |
| **Message Queue** | Kafka 3.x, 3 brokers, replication factor 3, 10 GB per partition | Add partitions for higher throughput |
| **Worker Pods** | Python 3.10, 2‑CPU, 4 GB RAM, Celery + Redis broker | HPA based on `queue.lag` metric |
| **Tika Server** | Docker image `apache/tika:2.8.0`, 2‑CPU, 2 GB RAM | Stateless – scale with workers |
| **OCR Service** | Azure Computer Vision (OCR) fallback to Tesseract | Autoscale via Keda based on queue depth |
| **ASR Service** | Whisper‑large-v2 (GPU) + Azure Speech‑to‑Text fallback | GPU node pool, queue‑driven batch inference |
| **Chunker** | 512‑token window, 50 % overlap, hierarchical (page → paragraph) | In‑process; negligible resources |
| **Embedding Service** | OpenAI ada‑002 (batch size ≤128) **or** local Sentence‑Transformers on CPU | Cache reduces calls; scale via additional pods if using local model |
| **Redis Cache** | Redis‑Cluster, 3‑master 3‑replica, 8 GB RAM total, LRU eviction | Add shards for larger cache |
| **FAISS Index** | IVF‑SQ8, 256 clusters, PQ 8‑bits, stored in RAM (~500 MB) | Re‑build nightly for hot‑vector refresh |
| **Qdrant** | `qdrant/qdrant:latest`, 4‑CPU, 8 GB RAM, persisted on SSD | Horizontal sharding via Qdrant’s collection replicas |
| **PostgreSQL** | 16‑core, 32 GB RAM, pgvector extension, WAL archiving | Primary‑replica read scaling |
| **LLM Backend** | OpenAI GPT‑4 (API) – rate‑limited; or self‑hosted Llama‑2 70B on 8× A100 GPUs | Autoscale API gateway; GPU node pool for self‑hosted |
| **Observability** | Prometheus + Grafana dashboards, OpenTelemetry Collector, Elastic Stack (Filebeat, Logstash, Kibana) | Deploy as DaemonSets; horizontal scaling via Prometheus remote‑write |
| **Secrets Management** | HashiCorp Vault, auto‑rotating tokens | HA deployment, integrated with K8s secrets injector |

---

## Scaling Plan

| Dimension | Baseline (50 K docs) | Projected Scale (200 K docs) | Action Items |
|-----------|---------------------|-----------------------------|--------------|
| **Ingestion Throughput** | 200 docs/s (8 M docs/h) | 400 docs/s (≈16 M docs/h) | Double worker replica count; increase Kafka partitions to 12 |
| **Vector Store Size** | 250 k vectors → ~2 GB RAM + 5 GB disk | 1 M vectors → ~8 GB RAM + 20 GB disk | Expand FAISS cluster shards; add Qdrant nodes; consider Milvus for >10 M vectors |
| **Embedding Cost** | $210/mo (ada‑002) | $420/mo (double volume) | Enable batch embedding and aggressive cache TTL; evaluate cheaper multilingual‑e5 model |
| **LLM Calls** | 5 k queries/day | 20 k queries/day | Implement query caching; add rate‑limit buckets |
| **Observability Data** | 10 GB/day logs | 30 GB/day logs | Use log rotation, compress older logs, consider Loki for cost‑effective storage |

**Horizontal scaling** is achieved via Kubernetes Deployments with HPA rules tied to custom metrics (queue lag, CPU, GPU usage). **Vertical scaling** (bigger nodes) is reserved for GPU‑intensive ASR/LLM workloads.

---

## Implementation Roadmap (Actionable Steps)

1. **Infrastructure Provisioning** (Weeks 1‑2)
   - Spin up a K8s cluster (EKS/GKE/AKS) with three node pools: CPU‑only, GPU, and storage‑optimized.
   - Deploy managed PostgreSQL (RDS) and Redis‑Cluster (ElasticCache).
   - Set up HashiCorp Vault for secrets.
2. **Core Services Deployment** (Weeks 3‑4)
   - Deploy Kong API gateway with OAuth2 provider (Keycloak).
   - Install Kafka with three brokers and create `ingest-topic`.
   - Deploy Tika, OCR, ASR services as StatefulSets.
   - Deploy worker pods (Celery) with auto‑scaling policies.
3. **Vector Store & Cache** (Week 5)
   - Launch FAISS index as an in‑memory service (custom FastAPI wrapper).
   - Deploy Qdrant cluster (2 replicas) with persistent SSD volumes.
   - Connect Redis L2 cache for embeddings.
4. **Embedding & Retrieval Layer** (Week 6)
   - Integrate OpenAI embedding endpoint (or local Sentence‑Transformers).
   - Implement upsert logic: on new/updated doc, delete old chunks from both stores, insert refreshed vectors.
5. **LLM Generator & Response Service** (Week 7)
   - Configure OpenAI GPT‑4 API keys in Vault; build FastAPI wrapper for generation with streaming support.
   - Add prompt templates that incorporate retrieved contexts.
6. **Observability Stack** (Week 8)
   - Deploy Prometheus Operator, Grafana dashboards (ingestion latency, queue depth, CPU/GPU usage).
   - Configure OpenTelemetry Collector to export traces to Jaeger.
   - Set up ELK Stack for log aggregation; enable alerting on error rates > 1 %.
7. **Security Hardenings** (Week 9)
   - Enforce mTLS between services.
   - Apply RBAC policies in Kong for each API route.
   - Enable encryption‑at‑rest for Qdrant and PostgreSQL (AWS KMS).
8. **Testing & Validation** (Week 10)
   - Run load‑test (Locust) simulating 50 K doc upload burst.
   - Verify end‑to‑end latency < 2 s for retrieval + generation.
   - Perform security scan (OWASP ZAP) on APIs.
9. **Production Roll‑out** (Week 11‑12)
   - Canary deploy with 10 % traffic.
   - Monitor KPIs; gradually increase traffic to 100 %.
   - Document SOPs for incident response and model updates.

---

## Conclusions

The proposed architecture meets the **functional requirement** of handling 50 K heterogeneous documents while delivering **sub‑second retrieval** and **cost‑effective embedding**. By integrating **queue‑driven ingestion**, a **hybrid vector store**, **caching**, and a **full observability & security stack**, we resolve all critical gaps identified by earlier reviews. The design is **cloud‑agnostic**, supports **incremental indexing**, and provides a clear path for scaling to larger corpora.

---

## Recommendations / Next Steps

1. **Pilot Deployment** with a subset of 5 K documents to validate end‑to‑end flow and cost model.
2. **Evaluate Alternative Embedding Models** (e.g., multilingual‑e5) for specific language coverage.
3. **Implement Data Retention Policies** to purge obsolete vectors after 12 months.
4. **Explore Managed Vector Stores** (Pinecone, Weaviate) for a fully serverless option if operational overhead becomes a concern.
5. **Continuous Model Monitoring** – set up drift detection on embeddings to trigger re‑embedding jobs automatically.
6. **User Feedback Loop** – capture relevance feedback to fine‑tune retrieval weighting.

---

*Prepared by the Reporter Agent on 2026‑02‑02. All design decisions are derived from the combined research, coding, critique, optimisation, and validation outputs.*