# MultiAgent-Chatbot

Generative AI–powered multi‑agent system that lets support teams query structured customer data and search policy PDFs using natural language.

## Demo Video
Watch the demo here: https://youtu.be/Ur58DUvFUoc

## Features
- Natural‑language queries over MySQL customer + ticket data
- Policy PDF ingestion into Chroma (vector store) for semantic search
- Multi‑agent routing (SQL vs. policy vs. both) using LangGraph
- Streamlit UI for interactive Q&A
- MCP server exposing tools for external clients

## Tech Stack
- **Python** + **Streamlit**
- **OpenAI** (LLM + embeddings)
- **MySQL** (structured data)
- **Chroma** (vector DB)
- **LangChain / LangGraph**
- **MCP** server

## Project Structure
```
app/
  agents.py          # LangGraph routing + agents
  config.py          # Environment settings
  db.py              # MySQL access helpers
  ingest.py          # PDF ingestion + Chroma vectorstore
  main.py            # Streamlit UI
data/
  policies/          # Policy PDFs
  sql/
    schema.sql       # MySQL schema
    seed.sql         # Sample data
scripts/
  init_db.py         # Create schema + seed data
  ingest_policies.py # Build Chroma index
mcp_server.py        # MCP server exposing tools
.env.example         # Environment template
requirements.txt
```

## Setup

### 1) Create a virtualenv (recommended)
```
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```
python3 -m pip install -r requirements.txt
```

### 3) Configure environment
Create `.env` from `.env.example` and set:
```
OPENAI_API_KEY=your_openai_key
MYSQL_HOST=Abus-MacBook-Air.local
MYSQL_PORT=3306
MYSQL_USER=Abu kalam Babuji
MYSQL_PASSWORD=29090112
MYSQL_DB=structured_DB
CHROMA_DIR=./chroma_db
POLICY_DIR=./data/policies
```

### 4) Initialize MySQL schema + seed data
```
python3 scripts/init_db.py
```

### 5) Add policy PDFs
Place policy PDFs in `data/policies/`.



### 6) Ingest policies into Chroma
```
PYTHONPATH=. python3 scripts/ingest_policies.py
```

### 7) Run the Streamlit app
```
streamlit run app/main.py
```

## Usage
Example questions:
- “What is the code of ethics for employees?”
- “Give me a quick overview of customer Abu's profile and past ticket details.”

## Architecture (High‑Level)
1. **Router agent** decides where to send the question:
   - SQL data
   - Policy documents
   - Both
2. **SQL agent** uses MySQL schema + LLM to generate and execute a query.
3. **Policy agent** retrieves relevant chunks from Chroma and answers.
4. **Final response** combines results based on the route.

```
User -> Streamlit UI
    -> LangGraph Router
      ├─ SQL Agent -> MySQL
      ├─ Policy Agent -> Chroma (PDF embeddings)
      └─ Final Response
```

## MCP Server
Run the MCP server (optional):
```
python3 mcp_server.py
```
Tools exposed:
- `get_customer_profile(name)`
- `get_customer_tickets(name)`
- `search_policies(query)`
- `policy://list` resource

## Troubleshooting
- **ModuleNotFoundError: app**  
  Run from repo root or use `PYTHONPATH=.`

- **LangChain import errors**  
  Upgrade:
  ```
  python3 -m pip install -U "langchain>=0.2" "langchain-community>=0.2" "langchain-openai>=0.1"
  ```

- **OpenAI quota error (429)**  
  Ensure your API key has active billing and quota.


