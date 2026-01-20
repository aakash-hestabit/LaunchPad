import json
import random
from pathlib import Path
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
from transformers import AutoTokenizer

RAW_DATA_DIR = Path("data/raw")
OUTPUT_DIR = Path("data")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)
MODEL_NAME = "mistralai/Mistral-7B-v0.1"
TARGET_SAMPLES = 1500
VAL_SPLIT = 0.1
MIN_TOKENS = 100
MAX_TOKENS = 512
SEED = 42
random.seed(SEED)

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    use_fast=True
)

def normalize_columns(df):

    df = df.rename(columns={
        "question": "input",
        "answer": "output"
    })

    df = df[["input", "output"]]
    df = df.dropna()
    df = df.drop_duplicates()
    return df

def build_instruction(sample_type):
    if sample_type == "qa":
        return "Answer the medical question accurately."
    if sample_type == "reasoning":
        return (
            "Explain the medical reasoning step by step "
            "and provide a clear conclusion."
        )
    if sample_type == "extraction":
        return "Extract the requested medical information from the text."


def create_sample(row, sample_type):

   
    instruction = build_instruction(sample_type)
    input_text = row["input"]
    output_text = row["output"]

    return {
        "sample_type": sample_type,
        "instruction": instruction,
        "input": input_text,
        "output": output_text
    }

def token_length(sample):
    text = (
        f"{sample['instruction']}\n"
        f"{sample['input']}\n"
        f"{sample['output']}"
    )
    return len(tokenizer.encode(text, add_special_tokens=False))

def load_and_process() -> list:

    all_samples = []

    for csv_file in RAW_DATA_DIR.glob("*.csv"):
        if csv_file.name == "medical_reasoning.csv":
            continue
        print(f"Loading: {csv_file.name}")
        df = pd.read_csv(csv_file)
        df = normalize_columns(df)

        for _, row in df.iterrows():
            sample_type = random.choice(["qa", "extraction"])

            all_samples.append(
                create_sample(row, sample_type)
            )

    return all_samples

def plot_overall_distribution(lengths):
    plt.figure(figsize=(10, 6))
    plt.hist(lengths, bins=50)
    plt.title("Overall Token Length Distribution")
    plt.xlabel("Number of Tokens")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("token_distribution.png")
    plt.close()

def plot_sample_type_distribution(samples):
    counts = defaultdict(int)

    for s in samples:
        counts[s["sample_type"]] += 1

    types = list(counts.keys())
    values = list(counts.values())

    plt.figure(figsize=(8, 6))
    plt.bar(types, values)
    plt.title("Sample Count by Type")
    plt.xlabel("Sample Type")
    plt.ylabel("Number of Samples")
    plt.tight_layout()
    plt.savefig("sample_type_distribution.png")
    plt.close()

def remove_sample_type(samples):
    cleaned = []
    for s in samples:
        s = s.copy()
        s.pop("sample_type", None)
        cleaned.append(s)
    return cleaned


def filter_by_token_length(samples):
    filtered = []
    
    for s in samples:
        if s['sample_type']!='reasoning':
            if MIN_TOKENS <= token_length(s) <= MAX_TOKENS:
                filtered.append(s)
        else:
            if MIN_TOKENS <= token_length(s) <= 1300:
                filtered.append(s)

    return filtered


def save_jsonl(samples, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

def load_reasoning_dataset(limit=500):
    path = RAW_DATA_DIR / "medical_reasoning.csv"
    df = pd.read_csv(path)

    df = df.rename(columns={
        "Question": "question",
        "Complex_CoT": "cot",
        "Response": "answer"
    })

    df = df.dropna()
    df = df.drop_duplicates()

    samples = []

    for _, row in df.iterrows():
        output_text = (
            f"{row['cot'].strip()}\n\n"
            f"Final Answer: {row['answer'].strip()}"
        )

        sample = {
            "sample_type":"reasoning",
            "instruction": (
                "Analyze the medical scenario step by step, "
                "clearly explain the clinical reasoning, "
                "and conclude with the most likely diagnosis or finding."
            ),
            "input": row["question"].strip(),
            "output": output_text
        }

        samples.append(sample)

    random.shuffle(samples)
    return samples[:limit]


if __name__ == "__main__":

    samples = load_and_process()

    samples = samples[:1700]

    reasoning_samples = load_reasoning_dataset(limit=600)

    samples.extend(reasoning_samples)

    samples = filter_by_token_length(samples)

    lengths = [token_length(s) for s in samples]
    
    plot_overall_distribution(lengths)

    random.shuffle(samples)

    samples = samples[:1200]

    plot_sample_type_distribution(samples)

    split_idx = int(len(samples) * (1 - VAL_SPLIT))
    train_samples = samples[:split_idx]
    val_samples = samples[split_idx:]

    train_samples = remove_sample_type(train_samples)
    val_samples = remove_sample_type(val_samples)

    save_jsonl(train_samples, OUTPUT_DIR / "train.jsonl")
    save_jsonl(val_samples, OUTPUT_DIR / "val.jsonl")