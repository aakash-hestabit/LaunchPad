# Quantisation Report

## Model
TinyLlama/TinyLlama-1.1B-Chat-v1.0 (LoRA fine-tuned)

## Formats Tested
BF16, INT8, INT4, GGUF bf16, GGUF f16, GGUF q8_0, GGUF q4_0

## Size Comparison
Format          |  Size (MB)
----------------|-------------
BF16            |    2102.13
INT8 (bnb)      |    1175.73
INT4 (bnb)      |     727.13
GGUF bf16       |    2099.05
GGUF f16        |    2099.05
GGUF q8_0       |    1115.62
GGUF q4_0       |     607.23
## Speed Comparison
| Format | Tokens/sec |
---------|-------------
BF16 | 40.48 tokens/sec
INT8 | 10.75 tokens/sec
INT4 | 18.30 tokens/sec
GGUF q8_0 | 11.18 tokens/sec
GGUF q4_0 | 19.91 tokens/sec
GGUF f16 | 7.83 tokens/sec
GGUF bf16 | 7.74 tokens/sec

## Quality Observations
- BF16: best quality
- INT8: no noticeable loss
- INT4: slight quality degradation
- GGUF: no noticable loss

## STEPS INVOLVED 

**Merge & Unload:** Integrating LoRA (Low-Rank Adaptation) weights back into the base model (TinyLlama) to create a standalone full-precision model.

**Conversion:** Transforming the model into the GGUF format for compatibility with llama.cpp.

**Quantization (GGUF):** Creating compressed versions (8-bit and 4-bit) specifically for CPU/GPU hybrid inference.

**Quantization (BitsAndBytes):** Using 4-bit (NF4) and 8-bit techniques for efficient GPU-only inference.

**Benchmarking:** Measuring the performance in terms of File Size and Tokens Per Second.

