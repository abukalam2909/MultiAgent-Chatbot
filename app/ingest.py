from __future__ import annotations

import json
from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma

from app.config import get_settings


def _load_sources(policy_dir: Path) -> dict:
    sources_path = policy_dir / "sources.json"
    if sources_path.exists():
        return json.loads(sources_path.read_text())
    return {}


def ingest_policies() -> int:
    settings = get_settings()
    policy_dir = Path(settings.policy_dir)
    policy_dir.mkdir(parents=True, exist_ok=True)

    sources = _load_sources(policy_dir)
    pdfs = sorted(policy_dir.glob("*.pdf"))
    if not pdfs:
        return 0

    docs = []
    for pdf in pdfs:
        loader = PyPDFLoader(str(pdf))
        pdf_docs = loader.load()
        for doc in pdf_docs:
            doc.metadata["source_file"] = pdf.name
            doc.metadata["source_url"] = sources.get(pdf.name, "")
        docs.extend(pdf_docs)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings()
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=settings.chroma_dir,
    )
    return len(chunks)


def get_vectorstore() -> Chroma:
    settings = get_settings()
    embeddings = OpenAIEmbeddings()
    return Chroma(
        embedding_function=embeddings,
        persist_directory=settings.chroma_dir,
    )
