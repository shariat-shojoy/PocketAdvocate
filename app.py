import streamlit as st

import components.navbar as navbar
import components.hero as hero
import components.wizard as wizard
st.set_page_config(

    page_title="Pocket Advocate",

    layout="wide"

)

# Load CSS
with open("assets/css/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

navbar.show()

hero.show()

wizard.show()