import streamlit as st
from services.legal_service import LegalService
import time

from components.result_card import show as result_card
from utils.parser import parse_sections


STEP_LABELS = [
    "Input Type",
    "Details",
    "Review",
    "Analyzing",
    "Results",
]


def _render_stepper(current_step):

    nodes = ""

    for i, label in enumerate(STEP_LABELS, start=1):

        if i < current_step:
            state = "completed"
            marker = "✓"
        elif i == current_step:
            state = "active"
            marker = str(i)
        else:
            state = ""
            marker = str(i)

        nodes += (
            f'<div class="step {state}">'
            f'<div class="step-line"></div>'
            f'<div class="step-circle">{marker}</div>'
            f'<div class="step-label">{label}</div>'
            f'</div>'
        )

    st.markdown(
        f'<div class="stepper">{nodes}</div>',
        unsafe_allow_html=True
    )


def show():

    # ---------- Session State ----------

    if "step" not in st.session_state:
        st.session_state.step = 1

    if "service" not in st.session_state:
        st.session_state.service = LegalService()

    if "input_type" not in st.session_state:
        st.session_state.input_type = None

    st.markdown(
        '<div class="card">'
        '<div class="eyebrow">Case Intake</div>'
        '<div class="section-title">Incident Analysis</div>'
        '<p class="card-subtext">'
        "Answer a few questions about what happened — we'll match it to the relevant "
        "sections of Bangladesh law."
        "</p>"
        "</div>",
        unsafe_allow_html=True
    )

    _render_stepper(st.session_state.step)

    # -----------------------------
    # STEP 1
    # -----------------------------

    if st.session_state.step == 1:

        st.subheader("Choose Input Type")

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "📝 Describe with Text",
                use_container_width=True
            ):

                st.session_state.input_type = "text"
                st.session_state.step = 2
                st.rerun()

        with col2:

            if st.button(
                "🖼 Upload Image",
                use_container_width=True
            ):

                st.session_state.input_type = "image"
                st.session_state.step = 2
                st.rerun()

    # -----------------------------
    # STEP 2
    # -----------------------------

    if st.session_state.step == 2:

        if st.session_state.input_type == "text":

            st.subheader("Describe the Incident")

            location = st.selectbox(
                "Where did it happen?",
                [
                    "Facebook",
                    "Messenger",
                    "WhatsApp",
                    "Street",
                    "Home",
                    "Workplace",
                    "School",
                    "Other"
                ]
            )

            person = st.text_input("Who was involved?")

            incident = st.text_area(
                "Describe what happened",
                placeholder="Example: Someone threatened to beat me if I reported him..."
            )

            when = st.text_input("When did it happen? (Optional)")

            st.session_state.user_query = f"""
Location:
{location}

Person:
{person}

Incident:
{incident}

Time:
{when}
"""

        else:

            st.subheader("Upload Evidence")

            uploaded = st.file_uploader(
                "Upload an image",
                type=["png", "jpg", "jpeg"]
            )

            if uploaded:

                st.image(uploaded, use_container_width=True)

                save_path = f"uploads/{uploaded.name}"

                with open(save_path, "wb") as f:
                    f.write(uploaded.getbuffer())

                st.session_state.image_path = save_path

                st.success("Image uploaded successfully.")

        left, right = st.columns(2)

        with left:

            if st.button("← Previous"):

                st.session_state.step = 1
                st.rerun()

        with right:

            if st.button("Next →"):

                if st.session_state.input_type == "text":

                    if incident.strip() == "":

                        st.warning("Please describe the incident.")

                    else:

                        st.session_state.step = 3
                        st.rerun()

                else:

                    if "image_path" not in st.session_state:

                        st.warning("Please upload an image.")

                    else:

                        st.session_state.step = 3
                        st.rerun()

    # -----------------------------
    # STEP 3
    # -----------------------------

    if st.session_state.step == 3:

        st.subheader("Review Your Information")

        if st.session_state.input_type == "text":

            st.code(st.session_state.user_query)

        else:

            st.image(
                st.session_state.image_path,
                use_container_width=True
            )

        col1, col2 = st.columns(2)

        with col1:

            if st.button("← Previous"):

                st.session_state.step = 2
                st.rerun()

        with col2:

            if st.button("🔎 Analyze Incident"):

                st.session_state.step = 4
                st.rerun()

    # -----------------------------
    # STEP 4
    # -----------------------------

    if st.session_state.step == 4:

        st.subheader("🤖 AI is Analyzing Your Incident")

        progress = st.progress(0)

        status = st.empty()

        steps = [
            "Validating input...",
            "Understanding the incident...",
            "Searching Bangladesh laws...",
            "Analyzing relevant legal sections...",
            "Preparing legal explanation..."
        ]

        for i, text in enumerate(steps):

            status.info(text)

            progress.progress((i + 1) / len(steps))

            time.sleep(0.5)

        try:

            if st.session_state.input_type == "text":

                answer = st.session_state.service.analyze_text(
                    st.session_state.user_query
                )

            else:

                answer = st.session_state.service.analyze_image(
                    st.session_state.image_path
                )

            st.session_state.answer = answer

            st.session_state.step = 5

            st.rerun()

        except Exception as e:

            st.error(f"Error: {e}")

            if st.button("⬅ Back"):

                st.session_state.step = 3

                st.rerun()

    # -----------------------------
    # STEP 5
    # -----------------------------

    if st.session_state.step == 5:

        st.success("Analysis Completed Successfully")

        tab1, tab2, tab3 = st.tabs(
            [
                "📋 Legal Analysis",
                "📚 Retrieved Context",
                "🖼 Evidence"
            ]
        )

        with tab1:

            answer = st.session_state.answer

            sections = parse_sections(answer)

            if sections:

                for title, content in sections.items():

                    result_card(
                        title,
                        "📌",
                        content
                    )

            else:

                result_card(
                    "Legal Analysis",
                    "⚖️",
                    answer
                )

        with tab2:

            try:

                with open(
                    "outputs/retrieved_context.txt",
                    "r",
                    encoding="utf-8"
                ) as f:

                    st.text(f.read())

            except Exception:

                st.info("No retrieved context available.")

        with tab3:

            if st.session_state.input_type == "image":

                st.image(
                    st.session_state.image_path,
                    use_container_width=True
                )

                try:

                    with open(
                        "outputs/image_analysis.txt",
                        "r",
                        encoding="utf-8"
                    ) as f:

                        st.subheader("Image Understanding")

                        st.write(f.read())

                except Exception:

                    pass

            else:

                st.write("Text-based incident")

                st.code(
                    st.session_state.user_query
                )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            if st.button("🔄 Start New Analysis"):

                for key in [
                    "step",
                    "input_type",
                    "user_query",
                    "image_path",
                    "answer"
                ]:

                    if key in st.session_state:
                        del st.session_state[key]

                st.rerun()

        with col2:

            try:

                with open(
                    "outputs/final_response.txt",
                    "r",
                    encoding="utf-8"
                ) as f:

                    st.download_button(
                        "📥 Download Report",
                        data=f.read(),
                        file_name="PocketAdvocate_Report.txt",
                        mime="text/plain"
                    )

            except Exception:

                st.button(
                    "📥 Download Report",
                    disabled=True
                )