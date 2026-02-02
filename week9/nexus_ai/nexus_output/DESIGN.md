# RAG Pipeline Architecture Design

## 1. Overview
The pipeline ingests heterogeneous documents (PDF, DOCX, HTML, images, audio, video), extracts textual content, converts it into dense vector embeddings, stores them in a scalable vector database, and finally performs Retrieval‑Augmented Generation (RAG) using a Large Language Model (LLM).

The design targets **up to 50 K documents** (average 2‑5 KB each) which translates to roughly **250 K‑500 K chunks** after splitting. This scale demands careful choices around parallelism, storage, and fault tolerance.

---

## 2. Component Diagram

```mermaid
flowchart TD
    subgraph Ingestion
        A[Document Source] -->|Fetch| B[Loader Layer]
        B -->|Extract Text| C[Text Extractor]
        C -->|OCR (if image) / ASR (if audio) | D[Enrichment Service]
    end
    subgraph Pre‑Processing
        D -->|Chunking| E[Chunker]
        E -->|Metadata Attach| F[Chunk Store (temporary DB)]
    end
    subgraph Embedding
        F -->|Batch| G[Embedding Service]
        G -->|Vectors| H[Vector Store]
    end
    subgraph Retrieval & Generation
        I[User Query] -->|Embed Query| J[Query Encoder]
        J -->|Nearest‑Neighbour Search| H
        H -->|Top‑K Chunks| K[Context Builder]
        K -->|Prompt + LLM| L[LLM Service]
        L -->|Response| M[API Gateway]
    end
    style Ingestion fill:#f9f,stroke:#333,stroke-width:2px
    style Pre‑Processing fill:#bbf,stroke:#333,stroke-width:2px
    style Embedding fill:#bfb,stroke:#333,stroke-width:2px
    style Retrieval & Generation fill:#ffb,stroke:#333,stroke-width:2px
```

---

## 3. Technology Choices
| Stage | Recommended Open‑Source / Cloud Options | Rationale |
|-------|----------------------------------------|-----------|
| **Document Source** | Cloud storage (AWS S3, GCS), SharePoint, Web crawlers | Unified access via SDKs |
| **Loader Layer** | `langchain.document_loaders`, `llama_index.readers` | Handles many formats; pluggable |
| **Text Extractor** | Apache Tika (Java, via REST), `pdfminer.six`, `python-docx` | Mature, supports metadata |
| **OCR** | Tesseract 5 (on‑prem), Azure Computer Vision, Google Document AI | Choose based on accuracy vs cost |
| **ASR** | OpenAI Whisper (local GPU), Azure Speech‑to‑Text, Google Speech API | Multilingual support |
| **Chunker** | LangChain `RecursiveCharacterTextSplitter`, custom hierarchical splitter | Configurable chunk size (e.g., 512 tokens) with 50 % overlap |
| **Embedding Service** | Sentence‑Transformers `mMiniLM‑L12‑v2` (384‑dim), multilingual‑e5, or OpenAI `text-embedding-ada-002` | Balance quality, latency, and storage |
| **Vector Store** | **Primary**: Milvus 2.x (IvfPQ) – disk‑based, sharding, horizontal scaling. **Fallback**: FAISS IVF‑SQ8 for dev/testing. | Milvus handles billions of vectors, supports persistence & replication |
| **LLM** | OpenAI GPT‑4o, Anthropic Claude, or self‑hosted Llama‑2 70B via vLLM | API‑first for ease of integration |
| **Orchestration** | Docker Compose for dev, Kubernetes (Helm chart) for prod. Use Airflow or Prefect for batch ingestion jobs. | Cloud‑native, autoscaling |
| **API Gateway** | FastAPI (Python) + Uvicorn, or Node.js Express; served behind NGINX/Traefik. | Async, OpenAPI spec |
| **Monitoring** | Prometheus + Grafana, OpenTelemetry, Loki for logs | Observability |

---

## 4. Data Flow
1. **Source Polling / Event Trigger** – A watcher (S3 event, webhook) pushes a file path to a message queue (RabbitMQ / Kafka).
2. **Loader** – Reads the raw bytes, determines MIME type, and delegates to a specific loader (PDF, HTML, etc.).
3. **Text Extraction** – For PDFs, use Tika; for images, run OCR; for audio/video, run ASR → transcript.
4. **Enrichment** – Attach metadata (source ID, timestamps, provenance) and language detection (fasttext). Optionally run entity extraction (SpaCy). 
5. **Chunking** – Split into overlapping chunks (default 512 tokens, 256 token stride). Each chunk gets a deterministic UUID: `hash(source_id + chunk_index)`.
6. **Embedding** – Batch‑process chunks (size 64‑128) through the embedding model; store vectors with metadata in Milvus collection `rag_chunks`.
7. **Index Refresh** – Milvus automatically builds IVF indices; schedule a `compact` operation nightly.
8. **Query Path** – User query arrives at FastAPI endpoint → embed via same model → Milvus `search` top‑k (k=5‑10) → retrieve raw text chunks → assemble prompt (`<system><retrieved>
<user>`). → send to LLM → stream response back.

---

## 5. Scaling Strategies
### 5.1 Ingestion Parallelism
- **Horizontal Workers**: Deploy multiple Celery workers (or Prefect agents) each consuming from the queue.
- **Batch Size Tuning**: Embedding batch size = 128; adjust based on GPU memory.
- **Back‑Pressure**: Use Kafka’s consumer groups with max poll records to avoid OOM.

### 5.2 Vector Store Scaling
- **Milvus Sharding**: Create 4 shards initially; each shard holds ~125 K vectors (~500 MB). Auto‑scale shards based on storage usage.
- **Index Type**: IVF‑PQ (nlist=4096, m=8) – good recall‑speed trade‑off for 384‑dim vectors.
- **Replication**: 2‑way replica for high availability; enable Raft consensus.
- **Cold Storage**: Archive older chunks to S3 and use Milvus “disk‑ann” to load on‑demand.

### 5.3 Retrieval & Generation
- **Cache Layer**: Redis LRU cache for recent query embeddings and search results (TTL 5 min).
- **Autoscaling**: Kubernetes HPA based on CPU/latency metrics of the FastAPI service.
- **LLM Rate Limiting**: Token bucket per user to protect external API quotas.

---

## 6. Sample Configuration (YAML)
```yaml
# config/pipeline.yaml
ingestion:
  source:
    type: s3
    bucket: rag-docs
    prefix: incoming/
  queue:
    broker: kafka://kafka:9092
    topic: rag_ingest
  workers: 8
  timeout_seconds: 300

processing:
  ocr:
    engine: azure_computer_vision
    endpoint: https://<region>.api.cognitive.microsoft.com/
    api_key: ${OCR_API_KEY}
  asr:
    engine: whisper
    device: cuda
  chunker:
    size_tokens: 512
    overlap_tokens: 256
    splitter: recursive
  embedding:
    model: sentence-transformers/mMiniLM-L12-v2
    batch_size: 128
    device: cuda
  vector_store:
    type: milvus
    host: milvus-standalone
    port: 19530
    collection: rag_chunks
    index_type: IVF_PQ
    metric: IP
    params:
      nlist: 4096
      m: 8
      nbits: 8

api:
  host: 0.0.0.0
  port: 8000
  timeout_seconds: 30
  rate_limit_per_minute: 60
  cors:
    origins: ["*"]

monitoring:
  prometheus_enabled: true
  otel_exporter: jaeger
  log_level: INFO
```

---

## 7. Deployment Sketch (Kubernetes Helm values)
```yaml
# helm/values.yaml
ingestion:
  replicaCount: 4
  resources:
    limits:
      cpu: "2"
      memory: "4Gi"
  env:
    - name: OCR_API_KEY
      valueFrom:
        secretKeyRef:
          name: rag-secrets
          key: ocr_api_key

vectorStore:
  milvus:
    replicaCount: 3
    resources:
      limits:
        cpu: "4"
        memory: "8Gi"
    persistence:
      enabled: true
      size: 100Gi

api:
  replicaCount: 2
  resources:
    limits:
      cpu: "1"
      memory: "2Gi"
  service:
    type: LoadBalancer
    port: 80
```

---

## 8. Security & Compliance
- **Secrets** stored in Kubernetes Secrets or Vault; never hard‑code.
- **Transport Encryption** – TLS for all HTTP/gRPC endpoints.
- **IAM** – Least‑privilege IAM roles for S3 bucket access.
- **Data Retention** – Configurable TTL for raw source files; automatic deletion after 90 days.
- **Audit Logging** – All ingestion events logged to centralized Loki with request IDs.

---

## 9. Operational Playbooks
| Task | Tool | Description |
|------|------|-------------|
| Index rebuild | Milvus `flush` + `compact` | Run nightly to reclaim space |
| Scaling workers | Kubernetes `kubectl scale deployment rag-ingest --replicas=12` | Adjust based on queue lag |
| Health checks | Prometheus alerts on latency > 2 s | Trigger PagerDuty |
| Data backup | `milvusctl backup` to S3 | Daily incremental |

---

## 10. Next Steps
1. **Prototype** – Spin up a Docker Compose stack with Tika, Milvus, FastAPI, and a small embedding model.
2. **Load Test** – Simulate 50 K docs ingestion using Locust to verify throughput.
3. **Cost Estimation** – Profile GPU/CPU usage for embedding and LLM calls.
4. **CI/CD** – Add GitHub Actions to lint YAML, build Docker images, and push Helm charts.

---

*This design is technology‑agnostic and can be adapted to managed services (Pinecone, Azure Cognitive Search) by swapping the `vector_store` section.*
