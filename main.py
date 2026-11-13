
import json
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent / "data"

# SemEval dataset: JSON Lines format
semeval = pd.read_json(
    DATA_DIR / "semeval2017_task7_pun.json",
    lines=True
)

# ExPUNations dataset: JSON array format
with open(DATA_DIR / "expunations_annotated_full.json", encoding="utf-8") as f:
    expunations = pd.DataFrame(json.load(f))

print("SemEval examples:", len(semeval))
print("ExPUNations annotations:", len(expunations))

# Merge using shared joke IDs
combined = semeval.merge(
    expunations,
    left_on="id",
    right_on="ID",
    how="inner",
    validate="one_to_one"
)

# Keep puns with usable human explanations
combined = combined[
    (combined["label"] == 1)
    & combined["Natural language explanation"].apply(
        lambda explanations: isinstance(explanations, list)
        and any(isinstance(e, str) and e.strip() for e in explanations)
    )
].copy()

print("\nMatched usable puns:", len(combined))
print("\nPun categories:")
print(combined["type"].value_counts())

# Export combined dataset
output = DATA_DIR / "combined_puns.json"

combined.to_json(
    output,
    orient="records",
    indent=2,
    force_ascii=False
)

print(f"\nSaved to: {output}")
