# code_app.py
# streamlit run code_app.py

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import time
import streamlit as st
from code_ai       import (
    generate_code, explain_code, find_and_fix_bugs,
    refactor_code, generate_tests, pair_program,
    analyse_code_quality, SUPPORTED_LANGUAGES,
    extract_code_blocks
)
from code_executor import execute_python

st.set_page_config(
    page_title="AI Code Generator",
    page_icon="⌨️",
    layout="wide"
)

# ── Session state ─────────────────────────────────────────────────────────────
if "chat_history"   not in st.session_state: st.session_state.chat_history   = []
if "generated_code" not in st.session_state: st.session_state.generated_code = ""

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("⌨️ AI Code Generator")
    st.caption("Your personal GitHub Copilot · Qwen2.5-VL")

    st.divider()

    language = st.selectbox("Primary language:", SUPPORTED_LANGUAGES, index=0)

    st.divider()
    st.markdown("**Quick prompts**")
    quick_prompts = [
        "Write a function to parse a CSV file",
        "Create a REST API endpoint with FastAPI",
        "Write a binary search algorithm",
        "Create a class for a bank account",
        "Write a function to validate email addresses",
        "Create a decorator for retry logic",
    ]

    # Use enumerate index for unique keys
    for i, qp in enumerate(quick_prompts):
        if st.button(qp, use_container_width=True, key=f"qp_{i}"):
            st.session_state["pending_generate"] = qp

    st.divider()
    if st.button("Clear chat history", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ── Main ──────────────────────────────────────────────────────────────────────
st.title("⌨️ AI Code Generator & Pair Programmer")
st.caption("Generate · Explain · Debug · Refactor · Test · Chat")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🚀 Generate",
    "📖 Explain",
    "🐛 Debug",
    "✨ Refactor",
    "🧪 Test",
    "💬 Pair Program"
])

# ── Tab 1: Generate ───────────────────────────────────────────────────────────
with tab1:
    st.subheader("Generate code from description")

    pending     = st.session_state.pop("pending_generate", None)
    description = st.text_area(
        "Describe what you want:",
        value   = pending or "",
        height  = 120,
        placeholder = "e.g. Write a Python function that reads a CSV file, "
                      "filters rows where age > 30, and returns a list of names"
    )
    context = st.text_area(
        "Existing code context (optional):",
        height      = 80,
        placeholder = "Paste any existing code the generated code should integrate with"
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        gen_lang     = st.selectbox("Language:", SUPPORTED_LANGUAGES, key="gen_lang")
    with col2:
        generate_btn = st.button("Generate code", type="primary", use_container_width=True)

    if generate_btn and description:
        with st.spinner("Generating code..."):
            result = generate_code(description, gen_lang, context)

        st.session_state.generated_code = result["primary_code"]

        for block in result["code_blocks"]:
            st.code(block["code"], language=block["language"])

        if gen_lang == "python" and result["primary_code"]:
            st.divider()
            if st.button("▶️ Run this code", key="run_generated"):
                with st.spinner("Executing..."):
                    exec_result = execute_python(result["primary_code"])
                if exec_result["success"]:
                    st.success("Code executed successfully")
                    if exec_result["output"]:
                        st.code(exec_result["output"], language="text")
                else:
                    st.error("Execution failed")
                    st.code(exec_result["error"], language="text")

        st.caption("Select all code above and copy · or use the copy icon top-right of code block")

# ── Tab 2: Explain ────────────────────────────────────────────────────────────
with tab2:
    st.subheader("Explain code in plain English")

    code_to_explain = st.text_area(
        "Paste code to explain:",
        height      = 250,
        placeholder = "Paste any code here..."
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        detail      = st.selectbox("Detail level:", ["brief", "standard", "detailed"])
    with col2:
        explain_btn = st.button("Explain", type="primary", use_container_width=True)

    if explain_btn and code_to_explain:
        with st.spinner("Analysing code..."):
            explanation = explain_code(code_to_explain, detail)
        st.markdown(explanation)

        st.divider()
        st.subheader("Code quality scores")
        with st.spinner("Scoring quality..."):
            quality = analyse_code_quality(code_to_explain, language)

        scores = quality.get("scores", {})
        if scores:
            cols = st.columns(len(scores))
            for col, (dim, score) in zip(cols, scores.items()):
                col.metric(dim.replace("_", " ").title(), f"{score}/10")
        st.markdown(quality["response"])

# ── Tab 3: Debug ──────────────────────────────────────────────────────────────
with tab3:
    st.subheader("Find and fix bugs")

    buggy_code = st.text_area(
        "Paste buggy code:",
        height      = 200,
        placeholder = "Paste code with bugs here..."
    )
    error_msg  = st.text_input(
        "Error message (optional):",
        placeholder = "e.g. TypeError: unsupported operand type(s) for +: 'int' and 'str'"
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        debug_lang = st.selectbox("Language:", SUPPORTED_LANGUAGES, key="debug_lang")
    with col2:
        debug_btn  = st.button("Find & fix bugs", type="primary", use_container_width=True)

    if debug_btn and buggy_code:
        with st.spinner("Analysing bugs..."):
            result = find_and_fix_bugs(buggy_code, error_msg, debug_lang)

        st.markdown(result["response"])

        if result["fixed_code"]:
            st.divider()
            st.subheader("Side by side comparison")
            col1, col2 = st.columns(2)
            with col1:
                st.caption("Original (buggy):")
                st.code(buggy_code, language=debug_lang)
            with col2:
                st.caption("Fixed:")
                st.code(result["fixed_code"], language=debug_lang)

# ── Tab 4: Refactor ───────────────────────────────────────────────────────────
with tab4:
    st.subheader("Refactor code for better quality")

    messy_code = st.text_area(
        "Paste code to refactor:",
        height      = 200,
        placeholder = "Paste working but messy code here..."
    )

    st.markdown("**Refactoring goals:**")
    goals = []
    col1, col2 = st.columns(2)
    with col1:
        if st.checkbox("Better variable names",     value=True,  key="ref_names"):  goals.append("Use clear descriptive variable names")
        if st.checkbox("Extract functions",         value=True,  key="ref_funcs"):  goals.append("Extract repeated logic into separate functions")
        if st.checkbox("Add type hints",            value=True,  key="ref_types"):  goals.append("Add type hints to all functions")
        if st.checkbox("Add docstrings",            value=True,  key="ref_docs"):   goals.append("Add docstrings to all functions and classes")
    with col2:
        if st.checkbox("Remove duplication",        value=True,  key="ref_dup"):    goals.append("Remove duplicated code")
        if st.checkbox("Improve error handling",    value=False, key="ref_err"):    goals.append("Add proper error handling and exceptions")
        if st.checkbox("Optimise performance",      value=False, key="ref_perf"):   goals.append("Optimise for better performance")
        if st.checkbox("Follow style guide",        value=True,  key="ref_style"):  goals.append("Follow language style guide")

    col1, col2 = st.columns([1, 3])
    with col1:
        ref_lang     = st.selectbox("Language:", SUPPORTED_LANGUAGES, key="ref_lang")
    with col2:
        refactor_btn = st.button("Refactor", type="primary", use_container_width=True)

    if refactor_btn and messy_code:
        with st.spinner("Refactoring..."):
            result = refactor_code(messy_code, ref_lang, goals)

        if result["refactored_code"]:
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Original")
                st.code(messy_code, language=ref_lang)
            with col2:
                st.subheader("Refactored")
                st.code(result["refactored_code"], language=ref_lang)

        st.divider()
        st.markdown(result["response"])

# ── Tab 5: Test ───────────────────────────────────────────────────────────────
with tab5:
    st.subheader("Generate unit tests")

    code_to_test = st.text_area(
        "Paste code to test:",
        height      = 200,
        placeholder = "Paste function or class to generate tests for..."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        test_lang = st.selectbox(
            "Language:",
            ["python", "javascript", "typescript"],
            key="test_lang"
        )
    with col2:
        framework = st.selectbox(
            "Framework:",
            ["pytest", "unittest"] if test_lang == "python" else ["jest", "mocha"]
        )
    with col3:
        test_btn = st.button("Generate tests", type="primary", use_container_width=True)

    if test_btn and code_to_test:
        with st.spinner("Writing tests..."):
            result = generate_tests(code_to_test, test_lang, framework)

        if result["test_code"]:
            st.code(result["test_code"], language=test_lang)
            if test_lang == "python":
                st.info(
                    "To run these tests:\n"
                    "1. Save as `test_your_module.py`\n"
                    "2. Run: `pytest test_your_module.py -v`"
                )
        else:
            st.markdown(result["response"])

# ── Tab 6: Pair programming chat ──────────────────────────────────────────────
with tab6:
    st.subheader("Pair programming chat")
    st.caption("Ask anything about code · Multi-turn · Context remembered")

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_msg = st.chat_input(f"Ask anything about {language} code...")

    if user_msg:
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.markdown(user_msg)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = pair_program(
                    user_msg,
                    st.session_state.chat_history[:-1],
                    language
                )
            st.markdown(response)

            # Run button for Python code in response — unique key using timestamp
            blocks         = extract_code_blocks(response)
            python_blocks  = [b for b in blocks if b["language"] == "python"]
            if python_blocks:
                run_key = f"run_chat_{int(time.time() * 1000)}"
                if st.button("▶️ Run this code", key=run_key):
                    exec_result = execute_python(python_blocks[0]["code"])
                    if exec_result["success"]:
                        st.success("Output:")
                        st.code(exec_result["output"])
                    else:
                        st.error("Error:")
                        st.code(exec_result["error"])

        st.session_state.chat_history.append({"role": "assistant", "content": response})