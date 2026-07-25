import streamlit as st


def show(title, icon, content):

    st.markdown(
        '<div class="card result-card">'
        "<h3>"
        f'<span class="icon-badge">{icon}</span>'
        f"{title}"
        "</h3>"
        "</div>",
        unsafe_allow_html=True
    )

    st.write(content)