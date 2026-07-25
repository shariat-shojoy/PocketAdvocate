import streamlit as st

def show(title, icon, content):

    st.markdown(
        f"""
        <div class="card">
            <h3>{icon} {title}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(content)