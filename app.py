import streamlit as st

from rag_pipeline import ask_campusquery


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CampusQuery",
    page_icon="🎓",
    layout="centered",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .source-box {
        padding: 12px 16px;
        border-radius: 10px;
        background-color: #f5f7fa;
        margin-bottom: 8px;
        border: 1px solid #e5e7eb;
    }

    .source-title {
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎓 CampusQuery</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Ask questions about VIT-AP using college documents"
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            sources = message.get("sources", [])

            if sources:

                st.markdown("### 📚 Sources")

                for source in sources:

                    st.markdown(
                        f"""
                        <div class="source-box">
                            <span class="source-title">
                                📄 {source['source']}
                            </span>
                            <br>
                            📑 Page {source['page']}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )


# ============================================================
# CHAT INPUT
# ============================================================

question = st.chat_input(
    "Ask something about VIT-AP..."
)


if question:

    # --------------------------------------------------------
    # User message
    # --------------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # --------------------------------------------------------
    # Assistant response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("🔍 Searching college documents..."):

            try:

                result = ask_campusquery(
                    question,
                    k=5
                )

                answer = result["answer"]
                sources = result["sources"]

                st.markdown(answer)

                # --------------------------------------------
                # Sources
                # --------------------------------------------

                if sources:

                    st.markdown("### 📚 Sources")

                    for source in sources:

                        st.markdown(
                            f"""
                            <div class="source-box">
                                <span class="source-title">
                                    📄 {source['source']}
                                </span>
                                <br>
                                📑 Page {source['page']}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                # Save assistant message
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                    }
                )

            except Exception as e:

                error_message = (
                    "Something went wrong while processing "
                    "your question."
                )

                st.error(error_message)

                st.exception(e)