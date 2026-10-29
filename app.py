import streamlit as st
from textwrap import dedent


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CampusQuery | AI Campus Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# HTML RENDERING HELPER
# IMPORTANT: Use st.html(), not st.markdown(), for HTML.
# ============================================================

def render_html(markup: str) -> None:
    st.html(dedent(markup).strip())


# ============================================================
# BLACK & RED CUSTOM THEME
# ============================================================

CUSTOM_CSS = """
<style>
:root {
    --bg: #08090d;
    --panel: #111218;
    --panel-hover: #191a22;
    --red: #ff334f;
    --red-light: #ff7184;
    --text: #f5f5f7;
    --muted: #999aa6;
    --border: rgba(255, 255, 255, 0.08);
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(
            ellipse at 85% 0%,
            rgba(255, 51, 79, 0.09),
            transparent 35%
        ),
        #08090d;
    color: var(--text);
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1320px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111218, #0b0c11);
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.4rem;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #d7d7e0;
}

.sidebar-brand {
    font-size: 27px;
    font-weight: 850;
    letter-spacing: -1.2px;
    color: #ffffff;
    margin-bottom: 3px;
}

.sidebar-brand span {
    color: var(--red);
}

.sidebar-caption {
    color: var(--muted);
    font-size: 10px;
    letter-spacing: 1.8px;
    text-transform: uppercase;
    margin-bottom: 24px;
}

/* Hero */

.hero {
    padding: 36px;
    border-radius: 22px;
    border: 1px solid rgba(255, 51, 79, 0.28);
    background:
        radial-gradient(
            circle at 95% 5%,
            rgba(255, 51, 79, 0.22),
            transparent 36%
        ),
        linear-gradient(125deg, #17171f, #0d0e13 70%);
    margin-bottom: 24px;
    overflow: hidden;
}

.hero-label {
    color: var(--red-light);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 15px;
}

.hero-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    margin-right: 8px;
    border-radius: 50%;
    background: var(--red);
    box-shadow: 0 0 12px rgba(255, 51, 79, 0.85);
}

.hero-title {
    color: #ffffff;
    font-size: clamp(36px, 5vw, 60px);
    line-height: 1.08;
    font-weight: 850;
    letter-spacing: -2px;
    margin: 0;
}

.hero-title span {
    color: var(--red);
}

.hero-description {
    color: #b0b0bd;
    font-size: 15px;
    line-height: 1.8;
    max-width: 760px;
    margin-top: 15px;
    margin-bottom: 22px;
}

.hero-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
}

.hero-tag {
    display: inline-block;
    color: #d9d9e2;
    background: rgba(255, 255, 255, 0.035);
    border: 1px solid rgba(255, 255, 255, 0.10);
    padding: 8px 12px;
    border-radius: 999px;
    font-size: 11px;
    font-weight: 600;
}

/* Dashboard cards */

.info-card {
    background: linear-gradient(145deg, #16171e, #101116);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 18px;
    min-height: 112px;
    margin-bottom: 10px;
    overflow-wrap: anywhere;
}

.info-card-label {
    color: #a0a1ae;
    font-size: 10px;
    font-weight: 750;
    letter-spacing: 1.3px;
    text-transform: uppercase;
}

.info-card-value {
    color: #ffffff;
    font-size: 21px;
    font-weight: 850;
    margin-top: 11px;
}

.info-card-note {
    color: #999aa6;
    font-size: 12px;
    line-height: 1.6;
    margin-top: 6px;
}

/* Section headings */

.section-heading {
    color: #f5f5f7;
    font-size: 19px;
    font-weight: 750;
    letter-spacing: -0.4px;
    margin: 18px 0 5px 0;
}

.section-description {
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 17px;
}

/* Chat */

[data-testid="stChatMessage"] {
    background: rgba(18, 19, 26, 0.88);
    border: 1px solid rgba(255, 255, 255, 0.075);
    border-radius: 16px;
    padding: 15px 18px;
    margin-bottom: 13px;
}

[data-testid="stChatMessage"] p {
    line-height: 1.8;
}

[data-testid="stChatInput"] {
    background: #111218;
    border: 1px solid rgba(255, 51, 79, 0.30);
    border-radius: 15px;
}

[data-testid="stChatInput"]:focus-within {
    border-color: var(--red);
    box-shadow: 0 0 0 1px rgba(255, 51, 79, 0.15);
}

[data-testid="stChatInput"] textarea {
    color: #ffffff;
}

/* Buttons */

.stButton > button {
    background: #15161d;
    border: 1px solid rgba(255, 255, 255, 0.10);
    color: #eeeeF3;
    border-radius: 12px;
    min-height: 43px;
    font-weight: 650;
    transition: all 0.18s ease;
}

.stButton > button:hover {
    background: #251219;
    border-color: var(--red);
    color: #ffffff;
}

/* Expanders and dividers */

[data-testid="stExpander"] {
    background: rgba(17, 18, 24, 0.85);
    border: 1px solid rgba(255, 255, 255, 0.09);
    border-radius: 12px;
}

hr {
    border-color: rgba(255, 255, 255, 0.09);
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Footer */

.footer {
    color: #777884;
    text-align: center;
    font-size: 10px;
    letter-spacing: 1px;
    line-height: 2;
    padding-top: 25px;
    padding-bottom: 10px;
}

@media (max-width: 700px) {
    .hero {
        padding: 24px 20px;
    }

    .hero-title {
        letter-spacing: -1px;
    }

    [data-testid="stMainBlockContainer"] {
        padding: 1rem 1rem 2rem;
    }
}
</style>
"""

# Render CSS directly. Do not send HTML or CSS through Markdown.
render_html(CUSTOM_CSS)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    render_html("""
        <div class="sidebar-brand">
            Campus<span>Query</span>
        </div>
        <div class="sidebar-caption">
            AI CAMPUS ASSISTANT
        </div>
    """)

    st.markdown("### Workspace")
    st.caption(
        "Explore campus information through your indexed documents."
    )

    retrieval_k = st.slider(
        "Retrieval depth",
        min_value=3,
        max_value=10,
        value=5,
        help="Number of document chunks retrieved for each question.",
    )

    st.divider()

    st.markdown("### Conversation")

    if st.button("＋ New conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_question = None
        st.rerun()

    st.divider()

    st.markdown("### Under the hood")

    render_html("""
        <div class="info-card">
            <div class="info-card-label">Language model</div>
            <div class="info-card-value">Groq</div>
            <div class="info-card-note">
                Grounded answer generation
            </div>
        </div>

        <div class="info-card">
            <div class="info-card-label">Retrieval engine</div>
            <div class="info-card-value">ChromaDB</div>
            <div class="info-card-note">
                Semantic document search
            </div>
        </div>

        <div class="info-card">
            <div class="info-card-label">Embedding model</div>
            <div class="info-card-value">BGE Small</div>
            <div class="info-card-note">
                BAAI/bge-small-en-v1.5
            </div>
        </div>
    """)

    st.caption(
        "Answers use retrieved passages and source references. "
        "Verify important academic decisions against official documents."
    )


# ============================================================
# HERO HEADER
# ============================================================

render_html("""
    <div class="hero">
        <div class="hero-label">
            <span class="hero-dot"></span>
            VIT-AP UNIVERSITY · KNOWLEDGE ASSISTANT
        </div>

        <div class="hero-title">
            Campus<span>Query</span>
        </div>

        <div class="hero-description">
            Your campus knowledge, one question away.
            Search academic regulations, examination information,
            student policies, and other indexed college documents
            through a conversational AI assistant.
        </div>

        <div class="hero-tags">
            <span class="hero-tag">
                ◉ Retrieval-Augmented Generation
            </span>
            <span class="hero-tag">
                ⌕ Semantic Search
            </span>
            <span class="hero-tag">
                ▤ Page-Level Sources
            </span>
            <span class="hero-tag">
                ✦ AI-Powered Answers
            </span>
        </div>
    </div>
""")


# ============================================================
# DASHBOARD SUMMARY
# ============================================================

question_count = sum(
    1
    for message in st.session_state.messages
    if message["role"] == "user"
)

col1, col2, col3 = st.columns(3)

with col1:
    render_html(f"""
        <div class="info-card">
            <div class="info-card-label">Your session</div>
            <div class="info-card-value">{question_count}</div>
            <div class="info-card-note">Questions asked</div>
        </div>
    """)

with col2:
    render_html(f"""
        <div class="info-card">
            <div class="info-card-label">Retrieval setting</div>
            <div class="info-card-value">Top {retrieval_k}</div>
            <div class="info-card-note">
                Passages retrieved per question
            </div>
        </div>
    """)

with col3:
    render_html("""
        <div class="info-card">
            <div class="info-card-label">Answer approach</div>
            <div class="info-card-value">Grounded AI</div>
            <div class="info-card-note">
                Answers with source references
            </div>
        </div>
    """)


# ============================================================
# SUGGESTED QUESTIONS
# ============================================================

if not st.session_state.messages:
    render_html("""
        <div class="section-heading">
            What would you like to know?
        </div>

        <div class="section-description">
            Choose a suggestion or type your own question below.
        </div>
    """)

    suggestions = [
        (
            "📅 Examination schedules",
            "What examination schedules are mentioned in the documents?",
        ),
        (
            "📚 Academic regulations",
            "Summarize the important academic regulations.",
        ),
        (
            "🎓 Attendance policies",
            "What do the documents say about attendance requirements?",
        ),
        (
            "🗂️ Student information",
            "Which documents contain important student information?",
        ),
    ]

    left, right = st.columns(2)

    with left:
        if st.button(
            suggestions[0][0],
            key="suggestion_0",
            use_container_width=True,
        ):
            st.session_state.pending_question = suggestions[0][1]
            st.rerun()

        if st.button(
            suggestions[2][0],
            key="suggestion_2",
            use_container_width=True,
        ):
            st.session_state.pending_question = suggestions[2][1]
            st.rerun()

    with right:
        if st.button(
            suggestions[1][0],
            key="suggestion_1",
            use_container_width=True,
        ):
            st.session_state.pending_question = suggestions[1][1]
            st.rerun()

        if st.button(
            suggestions[3][0],
            key="suggestion_3",
            use_container_width=True,
        ):
            st.session_state.pending_question = suggestions[3][1]
            st.rerun()


# ============================================================
# SOURCE DISPLAY
# ============================================================

def show_sources(sources, expanded=False):
    if not sources:
        return

    with st.expander(
        f"📚 Sources and page references ({len(sources)})",
        expanded=expanded,
    ):
        for index, source in enumerate(sources, start=1):
            source_name = str(
                source.get("source", "Unknown document")
            )
            page_number = source.get("page", "Unknown")

            st.markdown(f"**Source {index}**")
            st.text(source_name)
            st.caption(f"Page: {page_number}")

            if index < len(sources):
                st.divider()


# ============================================================
# CONVERSATION HISTORY
# ============================================================

render_html("""
    <div class="section-heading">Conversation</div>
""")

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="🎓"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="🔴"):
            st.markdown(message["content"])
            show_sources(message.get("sources", []))


# ============================================================
# CHAT INPUT
# ============================================================

typed_question = st.chat_input(
    "Ask about exams, regulations, attendance, deadlines..."
)

pending_question = st.session_state.pending_question
st.session_state.pending_question = None

question = pending_question or typed_question


# ============================================================
# PROCESS QUESTION THROUGH YOUR EXISTING RAG PIPELINE
# ============================================================

if question and question.strip():
    question = question.strip()

    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    with st.chat_message("user", avatar="🎓"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="🔴"):
        with st.spinner("Searching your campus knowledge base..."):
            try:
                # Keeps the RAG backend import until a question is asked.
                from rag_pipeline import ask_campusquery

                result = ask_campusquery(
                    question,
                    k=retrieval_k,
                )

                answer = result.get(
                    "answer",
                    "I couldn't generate an answer. Please try again.",
                )

                sources = result.get("sources", [])

                st.markdown(answer)
                show_sources(sources, expanded=True)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                })

            except Exception as exc:
                error_message = (
                    "CampusQuery couldn't process this question. "
                    "Please check your API key, vector database, "
                    "and embedding model configuration."
                )

                st.error(error_message)

                with st.expander("Troubleshooting details"):
                    st.code(str(exc))

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message,
                    "sources": [],
                })


# ============================================================
# FOOTER
# ============================================================

render_html("""
    <div class="footer">
        CAMPUSQUERY · AI-POWERED CAMPUS KNOWLEDGE
        <br>
        Verify important academic decisions against official university communications.
    </div>
""")