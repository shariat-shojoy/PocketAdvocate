import re

# pyrefly: ignore [missing-import]
import streamlit as st


def show(title, icon, content, card_key=None):

    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "section"
    unique_suffix = card_key or str(abs(hash(content[:50])))[:6]

    # Title sits outside the box — it's a label, not the outcome itself.
    st.markdown(
        '<div class="result-title">'
        f'<span class="icon-badge">{icon}</span>'
        f"{title}"
        "</div>",
        unsafe_allow_html=True
    )

    # The actual LLM-generated outcome gets visual weight in bordered container
    with st.container(key=f"outcome-{slug}-{unique_suffix}"):
        st.markdown(content)
