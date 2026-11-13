"""Read-only, paginated viewer for data/combined_puns.json."""

import json
from pathlib import Path

import streamlit as st


DATA_PATH = Path(__file__).resolve().parent / "data" / "combined_puns.json"
PAGE_SIZE = 25
PAGE_KEY = "jokes_page"
MISSING = object()


@st.cache_data(show_spinner=False)
def load_jokes(path, modified_ns):
    """Cache the data; the modification time invalidates stale cached results."""
    with Path(path).open(encoding="utf-8") as source:
        jokes = json.load(source)
    if not isinstance(jokes, list) or any(not isinstance(joke, dict) for joke in jokes):
        raise ValueError("Expected a JSON array of joke records.")
    return jokes


def change_page(offset, page_count):
    st.session_state[PAGE_KEY] = max(
        0, min(st.session_state[PAGE_KEY] + offset, page_count - 1)
    )


def navigation(position, page, page_count, total):
    previous, status, next_page = st.columns([1, 3, 1])
    with previous:
        st.button(
            "Previous",
            key=f"{position}_previous",
            disabled=page == 0,
            on_click=change_page,
            args=(-1, page_count),
        )
    with status:
        start = page * PAGE_SIZE + 1
        end = min((page + 1) * PAGE_SIZE, total)
        st.caption(f"Page {page + 1} of {page_count} · Jokes {start}–{end} of {total}")
    with next_page:
        st.button(
            "Next",
            key=f"{position}_next",
            disabled=page == page_count - 1,
            on_click=change_page,
            args=(1, page_count),
        )


def display_value(value):
    """Show stored values literally, distinguishing absent values from nulls."""
    if value is MISSING:
        return "[missing from JSON]"
    # Streamlit strips surrounding whitespace, so quote those strings explicitly.
    if isinstance(value, str) and value and value == value.strip():
        return value
    return json.dumps(value, ensure_ascii=False)


def render_joke(joke, number):
    st.subheader(f"Joke {number} · {display_value(joke.get('id', MISSING))}")
    st.text(display_value(joke.get("text", MISSING)))
    st.text(
        f"id: {display_value(joke.get('id', MISSING))} | "
        f"ID: {display_value(joke.get('ID', MISSING))}\n"
        f"Pun category (type): {display_value(joke.get('type', MISSING))} | "
        f"Classification label (label): {display_value(joke.get('label', MISSING))}"
    )

    # Every annotation array uses the same index as Annotator_IDs.
    metadata = {"text", "id", "ID", "type", "label", "Annotator_IDs"}
    fields = {key: value for key, value in joke.items() if key not in metadata}
    arrays = {key: value for key, value in fields.items() if isinstance(value, list)}
    annotators = joke.get("Annotator_IDs", MISSING)
    annotator_ids = annotators if isinstance(annotators, list) else []
    positions = max([len(annotator_ids), *(len(values) for values in arrays.values())])

    with st.expander(f"Human annotations · {len(annotator_ids)} annotators"):
        st.text(f"Annotator_IDs: {display_value(annotators)}")
        # Scalar fields and empty arrays must remain visible as supplied.
        for field, value in fields.items():
            if not isinstance(value, list) or not value:
                st.text(f"{field}: {display_value(value)}")

        if any(len(values) != len(annotator_ids) for values in arrays.values()):
            st.warning(
                "Annotation array lengths differ from Annotator_IDs. "
                "All positions are shown; absent values are marked explicitly."
            )

        for index in range(positions):
            annotator = annotator_ids[index] if index < len(annotator_ids) else MISSING
            with st.container(border=True):
                st.markdown(f"**Annotator {display_value(annotator)} · array index {index}**")
                for field, values in arrays.items():
                    value = values[index] if index < len(values) else MISSING
                    st.text(f"{field}: {display_value(value)}")

    st.divider()


def main():
    st.set_page_config(page_title="Pun viewer", layout="centered")
    st.title("Pun viewer")
    try:
        jokes = load_jokes(str(DATA_PATH), DATA_PATH.stat().st_mtime_ns)
    except (OSError, ValueError) as error:
        st.error(f"Could not load data/combined_puns.json: {error}")
        return

    if not jokes:
        st.info("No jokes in data/combined_puns.json.")
        return

    page_count = (len(jokes) + PAGE_SIZE - 1) // PAGE_SIZE
    page = max(0, min(st.session_state.get(PAGE_KEY, 0), page_count - 1))
    st.session_state[PAGE_KEY] = page

    navigation("top", page, page_count, len(jokes))
    start = page * PAGE_SIZE
    for index, joke in enumerate(jokes[start : start + PAGE_SIZE], start=start + 1):
        render_joke(joke, index)
    navigation("bottom", page, page_count, len(jokes))


if __name__ == "__main__":
    main()
