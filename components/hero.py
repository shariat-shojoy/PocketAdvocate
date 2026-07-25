import streamlit as st

# NOTE: these labels are placeholders meant to show the chip pattern.
# Replace with the law categories your LegalService actually covers
# before shipping — don't claim coverage the backend doesn't have.
COVERAGE_AREAS = [
    "Penal Code",
    "Digital Security Act",
    "Family & Domestic",
    "Labor Law",
    "Property Disputes",
]


def show():

    chips = "".join(
        f'<span class="chip">{area}</span>' for area in COVERAGE_AREAS
    )

    st.markdown(
        '<div class="card">'
        '<h1 class="main-title">Understand Your Legal Rights</h1>'
        '<p class="sub-title">'
        "Describe an incident in text or upload evidence. "
        "Pocket Advocate identifies potentially relevant Bangladesh laws "
        "and suggests possible legal next steps."
        "</p>"
        f'<div class="chip-row">{chips}</div>'
        "</div>",
        unsafe_allow_html=True
    )