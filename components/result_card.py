import re

import streamlit as st


def show(title, icon, content):

    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "section"

    # Title sits outside the box — it's a label, not the outcome itself.
    st.markdown(
        '<div class="result-title">'
        f'<span class="icon-badge">{icon}</span>'
        f"{title}"
        "</div>",
        unsafe_allow_html=True
    )

    # The actual LLM-generated outcome gets the visual weight: a real
    # bordered container (not just an adjacent styled div), targeted by
    # its key via the .st-key-outcome-* selector in style.css.
    with st.container(key=f"outcome-{slug}"):
        st.markdown(content)