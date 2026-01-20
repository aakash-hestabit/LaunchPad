from datasets import load_dataset

dataset = load_dataset(
    "FreedomIntelligence/medical-o1-reasoning-SFT", 
    "en", 
    split="train[:600]"
)


print(dataset[0])
print(f"\nDataset size: {len(dataset)}")
dataset.to_csv("data/raw/medical_reasoning.csv")