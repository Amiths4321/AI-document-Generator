# doc_app.py
# streamlit run doc_app.py

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from pathlib import Path
from doc_templates import get_document_types, get_template
from doc_ai        import generate_document, improve_section, translate_document
from doc_builder   import build_docx, build_txt, build_markdown

st.set_page_config(
    page_title="AI Document Generator",
    page_icon="📄",
    layout="wide"
)

# ── Session state ─────────────────────────────────────────────────────────────
if "generated_content" not in st.session_state: st.session_state.generated_content = ""
if "current_doc_type"  not in st.session_state: st.session_state.current_doc_type  = ""
if "field_values"      not in st.session_state: st.session_state.field_values      = {}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("📄 AI Document Generator")
    st.caption("Professional documents in seconds · Qwen2.5-VL")

    st.divider()

    doc_types = get_document_types()
    doc_type  = st.radio(
        "Document type:",
        doc_types,
        format_func=lambda x: f"{get_template(x).get('icon', '')} {x}"
    )

    st.divider()

    template = get_template(doc_type)
    st.caption(template.get("description", ""))

    use_rag = st.toggle(
        "Use TechCorp knowledge base",
        value=True,
        help="Enrich document with company-specific context from your RAG system"
    )

    st.divider()

    # Previously generated docs
    docs = list(Path("generated_docs").glob("*")) if Path("generated_docs").exists() else []
    if docs:
        st.markdown(f"**Generated docs:** {len(docs)}")
        if st.button("Open output folder", use_container_width=True):
            os.startfile(str(Path("generated_docs").absolute()))

# ── Main ──────────────────────────────────────────────────────────────────────
st.title(f"{template.get('icon', '📄')} {doc_type}")
st.caption(template.get("description", ""))

tab1, tab2, tab3 = st.tabs(["📝 Fill & Generate", "✏️ Edit & Download", "🌐 Translate"])

# ── Tab 1: Fill form and generate ─────────────────────────────────────────────
with tab1:
    st.subheader("Fill in the details")

    fields       = template.get("fields", [])
    field_values = {}

    # Render form fields
    for i, field in enumerate(fields):
        key   = field["key"]
        label = field["label"]
        ph    = field.get("placeholder", "")

        if field["type"] == "textarea":
            field_values[key] = st.text_area(
                label,
                height      = 100,
                placeholder = ph,
                key         = f"field_{doc_type}_{key}"
            )
        else:
            field_values[key] = st.text_input(
                label,
                placeholder = ph,
                key         = f"field_{doc_type}_{key}"
            )

    st.divider()

    # Generate button
    col1, col2 = st.columns([3, 1])
    with col1:
        generate_btn = st.button(
            "Generate Document",
            type             = "primary",
            use_container_width = True
        )
    with col2:
        clear_btn = st.button("Clear", use_container_width=True)

    if clear_btn:
        st.session_state.generated_content = ""
        st.rerun()

    if generate_btn:
        # Check required fields
        empty_fields = [
            f["label"] for f in fields
            if not field_values.get(f["key"], "").strip()
            and f.get("required", True)
        ]

        if len(empty_fields) > len(fields) // 2:
            st.warning("Please fill in at least half the fields for a good document.")
        else:
            with st.spinner("Generating your document... (this may take 30-60 seconds)"):
                result = generate_document(
                    doc_type,
                    template["prompt_template"],
                    field_values,
                    use_rag
                )

            st.session_state.generated_content = result["content"]
            st.session_state.current_doc_type  = doc_type
            st.session_state.field_values      = field_values

            col1, col2, col3 = st.columns(3)
            col1.metric("Word count",  result["word_count"])
            col2.metric("Doc type",    doc_type)
            col3.metric("RAG context", "Yes" if result["rag_used"] else "No")

            st.success("Document generated! Switch to the Edit & Download tab.")
            st.markdown(result["content"][:500] + "...")

# ── Tab 2: Edit and download ──────────────────────────────────────────────────
with tab2:
    if not st.session_state.generated_content:
        st.info("Generate a document first in the Fill & Generate tab.")
    else:
        st.subheader("Review and edit your document")

        # Editable text area
        edited_content = st.text_area(
            "Document content (edit as needed):",
            value  = st.session_state.generated_content,
            height = 500,
            key    = "edit_content"
        )

        st.divider()

        # Improve a section
        with st.expander("✨ Improve a specific section"):
            section_text = st.text_area(
                "Paste the section to improve:",
                height = 100,
                key    = "improve_section"
            )
            instruction = st.text_input(
                "How to improve it:",
                placeholder = "e.g. make it more formal / add more detail / simplify language"
            )
            if st.button("Improve section") and section_text and instruction:
                with st.spinner("Improving..."):
                    improved = improve_section(section_text, instruction)
                st.text_area("Improved version:", improved, height=150)
                st.info("Copy the improved text and paste it into the document above.")

        st.divider()

        # Download options
        st.subheader("Download")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📥 Download as Word (.docx)",
                         use_container_width=True, type="primary"):
                with st.spinner("Building Word document..."):
                    docx_path = build_docx(
                        edited_content,
                        st.session_state.current_doc_type
                    )
                with open(docx_path, "rb") as f:
                    st.download_button(
                        "Click to download .docx",
                        f.read(),
                        file_name = Path(docx_path).name,
                        mime      = "application/vnd.openxmlformats-officedocument"
                                    ".wordprocessingml.document",
                        key       = "dl_docx"
                    )
                st.success(f"Saved: {Path(docx_path).name}")

        with col2:
            md_content = f"# {st.session_state.current_doc_type}\n\n{edited_content}"
            st.download_button(
                "📥 Download as Markdown",
                md_content,
                file_name           = f"{st.session_state.current_doc_type.replace(' ', '_')}.md",
                mime                = "text/markdown",
                use_container_width = True,
                key                 = "dl_md"
            )

        with col3:
            st.download_button(
                "📥 Download as Text",
                edited_content,
                file_name           = f"{st.session_state.current_doc_type.replace(' ', '_')}.txt",
                mime                = "text/plain",
                use_container_width = True,
                key                 = "dl_txt"
            )

# ── Tab 3: Translate ──────────────────────────────────────────────────────────
with tab3:
    if not st.session_state.generated_content:
        st.info("Generate a document first in the Fill & Generate tab.")
    else:
        st.subheader("Translate document")

        languages = [
            "Hindi", "Marathi", "Tamil", "Telugu", "Kannada",
            "Bengali", "Gujarati", "French", "Spanish", "Arabic",
            "German", "Japanese", "Chinese (Simplified)"
        ]
        target_lang = st.selectbox("Translate to:", languages)

        if st.button("Translate", type="primary"):
            with st.spinner(f"Translating to {target_lang}..."):
                translated = translate_document(
                    st.session_state.generated_content,
                    target_lang
                )
            st.text_area(
                f"Translated document ({target_lang}):",
                translated,
                height = 400
            )
            st.download_button(
                f"Download {target_lang} version",
                translated,
                file_name = f"{st.session_state.current_doc_type}_{target_lang}.txt",
                mime      = "text/plain",
                key       = "dl_translated"
            )