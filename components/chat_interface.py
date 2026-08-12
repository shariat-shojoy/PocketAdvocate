"""The conversation screen and its per-message evidence attachments."""

from __future__ import annotations

import hashlib
from pathlib import Path
from uuid import uuid4

import streamlit as st

from components.result_card import show as result_card
from services.legal_service import LegalService
from utils.parser import parse_sections


UPLOAD_DIR = Path("uploads")
ALLOWED_IMAGE_TYPES = ["png", "jpg", "jpeg", "webp"]


@st.cache_resource
def get_legal_service():
    return LegalService()


def _new_draft():
    """Use fresh widget keys so Streamlit never reuses an old camera/upload value."""
    st.session_state.draft_images = []
    st.session_state.draft_text = ""
    st.session_state.draft_revision = st.session_state.get("draft_revision", 0) + 1


def _initialise_state():
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("draft_images", [])
    st.session_state.setdefault("draft_text", "")
    st.session_state.setdefault("draft_revision", 0)


def _save_attachment(upload, source):
    """Persist an uploaded image under a unique name and add it to this draft once."""
    if upload is None:
        return
    content = upload.getvalue()
    digest = hashlib.sha256(content).hexdigest()
    if any(item["digest"] == digest for item in st.session_state.draft_images):
        return

    UPLOAD_DIR.mkdir(exist_ok=True)
    suffix = Path(upload.name or "image.png").suffix.lower() or ".png"
    destination = UPLOAD_DIR / f"{uuid4().hex}{suffix}"
    destination.write_bytes(content)
    st.session_state.draft_images.append({
        "path": str(destination),
        "name": upload.name or "Camera photo",
        "source": source,
        "digest": digest,
    })


def _render_images(images, caption_prefix="Evidence"):
    columns = st.columns(min(3, len(images)))
    for index, image in enumerate(images):
        with columns[index % len(columns)]:
            if Path(image["path"]).exists():
                st.image(image["path"], caption=f"{caption_prefix}: {image['name']}")


def _render_history():
    for turn_index, message in enumerate(st.session_state.messages):
        role = message.get("role", "user")
        content = message.get("content", "")
        if role == "user":
            with st.chat_message("user", avatar="👤"):
                if content:
                    st.markdown(content)
                images = message.get("images", [])
                # Compatibility with messages created before multi-image support.
                if not images and message.get("image_path"):
                    images = [{
                        "path": message["image_path"],
                        "name": message.get("image_source", "Attached evidence"),
                        "source": message.get("image_source", "Attachment"),
                    }]
                if images:
                    _render_images(images)
        else:
            with st.chat_message("assistant", avatar="⚖️"):
                sections = parse_sections(content)
                if sections:
                    for section_index, (title, section_content) in enumerate(sections.items()):
                        result_card(title, "⚖️", section_content, card_key=f"msg_{turn_index}_{section_index}")
                else:
                    result_card("Legal analysis", "⚖️", content, card_key=f"msg_{turn_index}")


def _set_preset(text):
    st.session_state.draft_text = text
    st.session_state.draft_revision += 1


def show():
    _initialise_state()
    st.markdown(
        """<section class="hero-card">
        <p class="eyebrow">Bangladesh legal research assistant</p>
        <h1 class="main-title">Understand your legal rights</h1>
        <p class="sub-title">Ask in Bangla or English. Add one or more photos when visual evidence matters.</p>
        </section>""",
        unsafe_allow_html=True,
    )

    if st.session_state.messages:
        st.markdown('<div class="conversation-heading">Conversation</div>', unsafe_allow_html=True)
        _render_history()

    # Keep an empty response area above the composer. During streaming the reply
    # appears in its final position, so the composer does not jump above it.
    response_slot = st.container()
    revision = st.session_state.draft_revision

    with st.container(border=True):
        st.markdown("#### Ask a question")
        st.caption("Use a short description; attach photos only when they add evidence.")

        presets = st.columns(4)
        preset_values = [
            ("Cyber threat", "Someone is sending me threatening messages online."),
            ("Land dispute", "My neighbour has encroached on my property."),
            ("Workplace", "My employer terminated my job without notice."),
            ("Cheque fraud", "A signed cheque I received was dishonoured."),
        ]
        for index, (label, text) in enumerate(preset_values):
            with presets[index % 4]:
                if st.button(label, key=f"preset_{revision}_{index}", use_container_width=True, type="secondary"):
                    _set_preset(text)
                    st.rerun()

        query = st.text_area(
            "Your question",
            value=st.session_state.draft_text,
            height=110,
            placeholder="For example: What legal steps can I take after receiving these threats?",
            key=f"message_box_{revision}",
            label_visibility="collapsed",
        )
        st.session_state.draft_text = query

        upload_tab, camera_tab = st.tabs(["Upload photos", "Use camera"])
        with upload_tab:
            uploads = st.file_uploader(
                "Upload one or more images",
                type=ALLOWED_IMAGE_TYPES,
                accept_multiple_files=True,
                key=f"file_upload_{revision}",
            )
            for upload in uploads or []:
                _save_attachment(upload, "Upload")
        with camera_tab:
            camera_photo = st.camera_input("Take a new photo", key=f"camera_{revision}")
            _save_attachment(camera_photo, "Camera")

        if st.session_state.draft_images:
            st.markdown("**Evidence attached to this message**")
            preview_columns = st.columns(min(3, len(st.session_state.draft_images)))
            remove_index = None
            for index, image in enumerate(st.session_state.draft_images):
                with preview_columns[index % len(preview_columns)]:
                    st.image(image["path"], caption=image["name"])
                    if st.button("Remove", key=f"remove_{revision}_{index}", use_container_width=True):
                        remove_index = index
            if remove_index is not None:
                st.session_state.draft_images.pop(remove_index)
                st.rerun()

        send_clicked = st.button("Send message", key=f"send_{revision}", type="primary", use_container_width=True)

    if not send_clicked:
        return

    query = st.session_state.draft_text.strip()
    images = list(st.session_state.draft_images)
    if not query and not images:
        st.warning("Enter a question or attach at least one image.")
        return

    st.session_state.messages.append({"role": "user", "content": query, "images": images})
    with response_slot:
        with st.chat_message("user", avatar="👤"):
            if query:
                st.markdown(query)
            if images:
                _render_images(images)
        with st.chat_message("assistant", avatar="⚖️"):
            status = st.status("Reviewing evidence and searching relevant laws…", expanded=False)
            # Do not load PyTorch, the embedding model, and FAISS on page
            # startup. This keeps Railway's health check lightweight.
            answer = st.write_stream(
                get_legal_service().analyze_chat_stream(
                    history=st.session_state.messages[:-1],
                    text=query,
                    image_paths=[image["path"] for image in images],
                )
            )
            status.update(label="Analysis complete", state="complete", expanded=False)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    Path("outputs").mkdir(exist_ok=True)
    Path("outputs/final_response.txt").write_text(answer, encoding="utf-8")
    _new_draft()
    st.rerun()
