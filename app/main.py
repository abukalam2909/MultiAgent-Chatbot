import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Ensure project root is on sys.path when running via Streamlit
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.agents import build_graph
from app.config import get_settings
from app.ingest import ingest_policies, ingest_uploaded

load_dotenv()

st.set_page_config(page_title="Support Assistant", layout="wide")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Simple styling
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid;
    }
    .user-message {
        background-color: rgba(59, 130, 246, 0.1);
        border-color: #3b82f6;
    }
    .assistant-message {
        background-color: rgba(156, 163, 175, 0.1);
        border-color: #9ca3af;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.title("Support Assistant")
st.markdown("Ask questions about customers or policy documents")

# Sidebar - just the essentials
with st.sidebar:
    st.header("Policy Documents")
    
    if st.button("Load Default Policies"):
        with st.spinner("Loading..."):
            count = ingest_policies()
            st.success(f"Loaded {count} chunks")
    
    st.divider()
    
    uploads = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)
    if uploads and st.button("Process Uploads"):
        with st.spinner("Processing..."):
            saved_paths = []
            policy_dir = Path(get_settings().policy_dir)
            policy_dir.mkdir(parents=True, exist_ok=True)
            for uploaded in uploads:
                target = policy_dir / uploaded.name
                target.write_bytes(uploaded.read())
                saved_paths.append(target)
            count = ingest_uploaded(saved_paths)
            st.success(f"Loaded {count} chunks")
    
    st.divider()
    
    # Clear history button
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

# Display chat history
if st.session_state.messages:
    st.markdown("### Conversation History")
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-message user-message"><strong>Q:</strong> {msg["content"]}</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message assistant-message"><strong>A:</strong> {msg["content"]}</div>', 
                       unsafe_allow_html=True)
    st.divider()

# Main area
question = st.text_input("Your question:", placeholder="What is the code of ethics for employees?")

if st.button("Ask", type="primary"):
    if question:
        with st.spinner("Thinking..."):
            graph = build_graph()
            result = graph.invoke({"question": question, "route": None})
            answer = result.get("final", "No response.")
            
            # Add to history
            st.session_state.messages.append({"role": "user", "content": question})
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
            st.rerun()
    else:
        st.warning("Please enter a question")

# Quick examples
st.divider()
st.markdown("**Example questions:**")
col1, col2 = st.columns(2)
with col1:
    st.markdown("• What is the code of ethics for employees?")
    st.markdown("• What are the leave policies?")
with col2:
    st.markdown("• Give me an overview of customer Abu's profile")
    st.markdown("• Show recent support tickets for John")