import time
import torch
import psutil
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer, util

BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
FT_MODEL = "./quantized/merged_model"
GGUF_MODEL = "./quantized/model-q8_0.gguf"
PROMPTS = [
    """### Instruction:
Answer the medical question accurately.

### Input:
What are the treatments for Heart Attack ?

### Response:
""",

    """### Instruction:
Answer the medical question accurately.

### Input:
What is (are) Low Vision ?

### Response:
""",

    """### Instruction:
Answer the medical question accurately.

### Input:
Is Ovarian Epithelial, Fallopian Tube, and Primary Peritoneal Cancer inherited ?

### Response:
"""
]

GROUND_TRUTH = [
    "Heart attack treatment focuses on quickly restoring blood flow using thrombolytic drugs or angioplasty, followed by cardiac rehabilitation, lifestyle changes, and medications to prevent further damage.",

    "People with low vision can receive support services such as vision rehabilitation, counseling, recreation programs, and job training through community and state agencies for the visually impaired.",

    "About 20% of ovarian, fallopian tube, and primary peritoneal cancers are caused by inherited gene mutations, often associated with breast or colon cancer, and genetic testing is recommended for high-risk families."
]



DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
RESULTS_PATH = "./benchmarks/results.csv"

embedder = SentenceTransformer("BAAI/bge-base-en-v1.5")


def get_vram():
    if torch.cuda.is_available():
        return torch.cuda.memory_allocated() / 1024**2
    return 0

def accuracy(preds, refs):
    p_emb = embedder.encode(preds, convert_to_tensor=True)
    r_emb = embedder.encode(refs, convert_to_tensor=True)

    sims = util.cos_sim(p_emb, r_emb)

    per_sample_scores = sims.diag().cpu().numpy()

    # for i, score in enumerate(per_sample_scores):
    #     print(f"Sample {i+1} Similarity: {score:.3f}")

    mean_score = per_sample_scores.mean()

    return mean_score


def benchmark_hf(model_path, label, batch=True, streaming=False):
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, device_map=DEVICE
    )

    inputs = tokenizer(PROMPTS, return_tensors="pt", padding=True).to(DEVICE)

    torch.cuda.synchronize() if DEVICE == "cuda" else None

    start = time.time()

    
    out = model.generate(**inputs, max_new_tokens=128)

    torch.cuda.synchronize() if DEVICE == "cuda" else None
    end = time.time()

    responses = [
        tokenizer.decode(o, skip_special_tokens=True)
        for o in out
    ]

    tokens = sum(len(tokenizer.encode(r)) for r in responses)
    tps = tokens / (end - start)
    acc = accuracy(responses, GROUND_TRUTH)
    # print(responses)
    # print(f'\n \n')

    return {
        "Model": label,
        "Tokens/sec": round(tps, 2),
        "Latency(s)": round(end - start, 2),
        "VRAM(MB)": round(get_vram(), 2),
        "Accuracy": round(acc, 3)
    }

def benchmark_gguf(label):
    llm = Llama(model_path=GGUF_MODEL, n_ctx=2048, n_threads=8, verbose=False)

    start = time.time()
    outputs = []

    for p in PROMPTS:
        out = llm(p, max_tokens=128)
        outputs.append(out["choices"][0]["text"])

    end = time.time()

    tokens = sum(len(o.split()) for o in outputs)
    tps = tokens / (end - start)
    acc = accuracy(outputs, GROUND_TRUTH)
    # print(outputs)

    return {
        "Model": label,
        "Tokens/sec": round(tps, 2),
        "Latency(s)": round(end - start, 2),
        "VRAM(MB)": round(get_vram(), 2),
        "Accuracy": round(acc, 3)
    }


results = []

results.append(benchmark_gguf("GGUF Q8 llama.cpp"))
results.append(benchmark_hf(BASE_MODEL, "Base Model"))
results.append(benchmark_hf(FT_MODEL, "Fine-tuned"))


df = pd.DataFrame(results)
df.to_csv(RESULTS_PATH, mode='a', index=False)

print(df)