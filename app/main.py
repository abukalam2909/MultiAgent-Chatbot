import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Ensure project root is on sys.path when running via Streamlit
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.agents import build_graph
from app.ingest import ingest_policies

load_dotenv()

st.set_page_config(page_title="Support Multi-Agent Assistant", layout="wide")

st.title("Support Multi-Agent Assistant")

with st.sidebar:
    st.header("Setup")
    if st.button("Ingest policy PDFs"):
        count = ingest_policies()
        st.success(f"Ingested {count} chunks into Chroma.")
    st.caption("Make sure OPENAI_API_KEY and MySQL settings are set in .env")

question = st.text_input("Ask a question about customers or policy documents")

if st.button("Ask") and question:
    graph = build_graph()
    result = graph.invoke({"question": question, "route": None})
    st.markdown(result.get("final", "No response."))

st.divider()

st.subheader("Example questions")
examples = [
    "What is the code of ethics for employees?",
    "Give me a quick overview of customer Abu's profile and past ticket details.",
]
for ex in examples:
    st.write(f"- {ex}")
