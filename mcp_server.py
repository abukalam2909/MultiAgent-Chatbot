import json
from pathlib import Path

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

from app.config import get_settings
from app.db import run_query
from app.ingest import get_vectorstore

load_dotenv()

mcp = FastMCP("Support MCP Server", json_response=True)


@mcp.tool()
def get_customer_profile(name: str) -> list:
    """Lookup a customer by name (partial matches allowed)."""
    sql = (
        "SELECT id, name, email, phone, city, status, created_at "
        "FROM customers WHERE name LIKE :name"
    )
    return run_query(sql, {"name": f"%{name}%"})


@mcp.tool()
def get_customer_tickets(name: str) -> list:
    """List tickets for a customer by name."""
    sql = (
        "SELECT t.id, t.subject, t.category, t.status, t.priority, t.opened_at, "
        "t.closed_at, t.summary "
        "FROM tickets t JOIN customers c ON t.customer_id = c.id "
        "WHERE c.name LIKE :name"
    )
    return run_query(sql, {"name": f"%{name}%"})


@mcp.tool()
def search_policies(query: str) -> str:
    """Search policy documents and return top snippets."""
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(query)
    snippets = []
    for d in docs:
        snippet = d.page_content[:600].replace("\n", " ")
        source = d.metadata.get("source_file", "")
        snippets.append(f"[{source}] {snippet}")
    return "\n\n".join(snippets)


@mcp.resource("policy://list")
def list_policies() -> str:
    """List available policy PDFs."""
    settings = get_settings()
    sources_path = Path(settings.policy_dir) / "sources.json"
    if not sources_path.exists():
        return json.dumps([])
    return sources_path.read_text()


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
