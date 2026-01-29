# Agent Memory System

## Memory Layers

| Memory | Purpose | Implementation |
|--------|---------|----------------|
| Short-Term Memory | Keeps recent conversation context | Rolling in-memory buffer of recent user and agent messages |
| Long-Term Memory | Stores durable user facts | SQLite table storing atomic facts with metadata |
| Vector Memory | Enables semantic recall | FAISS index storing embeddings linked to memory IDs |

---

## Memory Ingestion

- Fact Extraction - LLM extracts only long-term user-related facts from conversations  
- Noise Filtering - Small talk and conversation flow are ignored by prompt design  
- Importance Filtering - Facts with low importance scores are discarded  
- Atomic Storage - Each memory is stored as an independent factual statement  

---

## Memory Reconciliation

- Similarity Gating - Only related facts are compared using cosine similarity thresholds  
- Duplicate Detection - Highly similar facts are ignored to prevent repetition  
- Contradiction Handling - Conflicting old facts are deleted and replaced with new ones  
- Fact Updating - Newer information replaces outdated memory entries  
- Fact Merging - Related facts are combined into one concise memory  
- Canonical Replacement - Old memory is removed so only one valid version remains  

---

## Retrieval Process

- Query Embedding - User query converted into a vector representation  
- Vector Search - FAISS retrieves semantically similar memories  
- Similarity Filtering - Only memories above a threshold are used  
- Context Injection - Session memory and relevant facts are added to the prompt  
- Prompt Control - Only top relevant facts are injected to limit token usage  

---

## System Features

- Persistent memory across sessions  
- Semantic similarity search instead of keyword matching  
- Memory deduplication and contradiction prevention  
- Importance-based knowledge filtering  
- Clean and scalable hybrid memory architecture  
- Safe JSON extraction from LLM responses  

---

## Flow
```
New Query
    |
Retrieve Session Memory (recent conversation)
    |
Embed Query → Vector Search in FAISS
    |
Filter by Similarity Threshold
    |
Fetch Matching Facts from SQLite
    |
Inject Session Context + Relevant Facts into Prompt
    |
LLM Generates Response
    |
Extract Long-Term User Facts from Interaction
    |
Importance Filtering (discard low-value facts)
    |
Similarity Gating with Existing Memories
    |
Reconciliation (Duplicate / Merge / Update / Contradiction Handling)
    |
Store Canonical Facts in SQLite + FAISS
```

---  