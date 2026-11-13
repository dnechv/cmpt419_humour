# Pun dataset viewer

From this directory (`/Users/dvn/Desktop/SFU/Fall2026/cmpt419/project/code`):

```sh
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m streamlit run viewer.py
```

If `.venv` does not exist, create it first with `python3 -m venv .venv`
(Python 3.9 or later). Open the local URL printed by Streamlit, usually
http://localhost:8501. Stop the viewer with Ctrl+C.

The viewer reads the existing `data/combined_puns.json` in its original order
and displays 25 jokes per page. Use **Previous** and **Next** above or below
the jokes. The current 1,712-record dataset has 69 pages; the last has 12 jokes.
Each joke shows its text, ID, pun type, label, all human explanations, and all
other annotation fields. Explanation numbers and annotation-list positions
match `Annotator_IDs`. Blank explanation slots say **No explanation provided**,
and each joke shows how many explanation slots contain text. Zeroes and nested
keyword lists are preserved. There are no search boxes, filters, or charts.

The annotations are displayed as supplied. For example, `het_16` already has
four blank explanations and an unrelated bored/board explanation in
`data/expunations_annotated_full.json`. Such source-data mismatches need review
before correcting the dataset.

The viewer resolves the data path relative to `viewer.py`, so it also works
when launched from another directory using the full path to the script.
It does not write to the dataset. `main.py` is the separate dataset-building
script and overwrites `data/combined_puns.json` when run; it is not needed to
view the existing data.

To check syntax without running the dataset builder:

```sh
.venv/bin/python -c "import ast; from pathlib import Path; [ast.parse(Path(name).read_text(encoding='utf-8'), filename=name) for name in ('viewer.py', 'main.py')]; print('Python syntax OK')"
```
