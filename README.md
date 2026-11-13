# CMPT 419 — Computational Humour Project

A Python-based dataset viewer for exploring pun jokes and their human annotations.


## Installation

**1. Clone the repository**

```bash
git clone https://github.com/dnechv/cmpt419_humour.git
cd cmpt419_humour
```

**2. Create a virtual environment**

```bash
python3 -m venv .venv
```

**3. Activate the virtual environment**

macOS / Linux:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

**4. Install dependencies**

```bash
python -m pip install -r requirements.txt
```

## Running the Dataset Viewer

Start the Streamlit application:

```bash
python -m streamlit run viewer.py
```

Open the local URL displayed in the terminal, usually:

http://localhost:8501

To stop the application, press `Ctrl+C`.

## Running It Again

After the initial installation, simply activate your virtual environment and start the viewer:

```bash
source .venv/bin/activate
python -m streamlit run viewer.py
```

The viewer uses `data/combined_puns.json` and does not modify the dataset.