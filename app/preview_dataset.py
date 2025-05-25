import json

file_path = "finetune_dataset.jsonl"

try:
    with open(file_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            data = json.loads(line)
            print(f"\n🔹 Sample {i+1}:\n")
            print(json.dumps(data, indent=2))
            if i == 2:
                break  # show first 3 samples only
except FileNotFoundError:
    print(f"❌ File not found: {file_path}")