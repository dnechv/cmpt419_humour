"""Select and assign 150 SemEval puns for the CMPT 419 project.

From the project/code directory, run:
    python3 select_150_jokes.py

Input:  data/combined_puns.json
Output: data/selected_150_jokes.csv
Requires: pandas
"""

from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parent / "data"
SOURCE = DATA_DIR / "combined_puns.json"
OUTPUT = DATA_DIR / "selected_150_jokes.csv"

# The same random selection and 19/18 assignment split Lana proposed.
SEED = 42
MEMBERS = [
    "Mrinal Goshalia",
    "Lana Alsheikh",
    "Dhwani Patel",
    "Dmitry Nechvolod",
]
DISPLAY_ORDER = [
    "Lana Alsheikh",
    "Dmitry Nechvolod",
    "Mrinal Goshalia",
    "Dhwani Patel",
]


def main() -> None:
    eligible_df = pd.read_json(SOURCE)
    required_columns = {"ID", "text", "type"}
    missing = required_columns - set(eligible_df.columns)
    if missing:
        raise ValueError(f"Input missing required columns: {sorted(missing)}")
    if eligible_df["ID"].isna().any() or not eligible_df["ID"].is_unique:
        raise ValueError("Input contains missing or duplicate joke IDs")

    # Select 75 jokes independently from each pun category.
    homo = eligible_df[eligible_df["type"] == "homographic"].sample(
        n=75, random_state=SEED
    ).copy()
    hetero = eligible_df[eligible_df["type"] == "heterographic"].sample(
        n=75, random_state=SEED
    ).copy()

    # Fair distribution: two members get 38 and two get 37 jokes.
    homo["Member"] = (
        [MEMBERS[0]] * 19 + [MEMBERS[1]] * 19
        + [MEMBERS[2]] * 19 + [MEMBERS[3]] * 18
    )
    hetero["Member"] = (
        [MEMBERS[0]] * 19 + [MEMBERS[1]] * 19
        + [MEMBERS[2]] * 18 + [MEMBERS[3]] * 19
    )

    selected = pd.concat([homo, hetero], ignore_index=True)

    # Check the requested sample before writing anything.
    assert len(selected) == 150
    assert selected["ID"].is_unique, "Duplicate joke IDs in the selection"
    assert selected["type"].value_counts().to_dict() == {
        "homographic": 75, "heterographic": 75
    }

    # Organization only: Lana, Dmitry, Mrinal, Dhwani;
    # within each member, homographic first, heterographic second.
    selected["Member"] = pd.Categorical(
        selected["Member"], categories=DISPLAY_ORDER, ordered=True
    )
    selected["type"] = pd.Categorical(
        selected["type"],
        categories=["homographic", "heterographic"],
        ordered=True,
    )
    selected = selected.sort_values(
        ["Member", "type", "ID"], kind="stable"
    ).reset_index(drop=True)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    selected[["ID", "text", "type", "Member"]].to_csv(
        OUTPUT, index=False, encoding="utf-8-sig"
    )
    print(pd.crosstab(selected["Member"], selected["type"]))
    print(f"Saved {len(selected)} jokes to {OUTPUT}")


if __name__ == "__main__":
    main()
