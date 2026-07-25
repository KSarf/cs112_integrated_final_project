"""Starter Streamlit app for synthetic grid analysis."""

from __future__ import annotations

import streamlit as st


def main() -> None:
    """Render starter dashboard content."""
    st.set_page_config(page_title="Grid Analysis Dashboard", layout="wide")
    st.title("National Electricity Grid Network Analysis")
    st.info("Data in this dashboard is synthetic and for coursework only.")

    view = st.sidebar.radio(
        "Navigation",
        ["Overview", "Network", "Geography", "Reliability"],
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Nodes", "TODO")
    col2.metric("Edges", "TODO")
    col3.metric("Reliability Index", "TODO")

    st.subheader(view)
    st.write("TODO: Implement this dashboard section.")


if __name__ == "__main__":
    main()
