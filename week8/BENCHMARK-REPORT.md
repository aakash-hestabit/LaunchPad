# Benchmark Report

## Models Tested
- Base TinyLlama 1.1B Chat
- Fine-tuned LoRA merged
- GGUF Q8 (llama.cpp)

## Metrics
- Tokens/sec
- Latency
- VRAM usage
- Accuracy (semantic similarity)

## Results Summary

Below are the results produced when inferencing was perofrmed on Local Machine :

| Model | Tokens/sec | Latency | VRAM | Accuracy |
|------|------------|---------|------|----------|
| GGUF Q8 | 26.06 | 11.3s | 0 | 0.755 |
| Base | 14.12 | 29.11s | 0 | 0.765 |
| Fine-tuned | 17.85 | 28.51s | 0 | 0.76 |

<hr>

Below are the results produced when inferencing was perofrmed on Kaggle using T4 GPU :

![gpu inference benchmarks](image-3.png)

---

Below are the results produced when inferencing was perofrmed on Kaggle using T4 GPU with streaming on :

![gpu inference kaggle streaming](image-4.png)