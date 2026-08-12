# pyrefly: ignore [missing-import]
import streamlit as st

import components.navbar as navbar
import components.chat_interface as chat_interface

st.set_page_config(
    page_title="Pocket Advocate — AI Legal Assistant",
    page_icon="⚖️",
    layout="wide"
)

# Load CSS
with open("assets/css/style.css", "r", encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

navbar.show()

chat_interface.show()
