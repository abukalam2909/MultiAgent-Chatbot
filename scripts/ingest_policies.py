from dotenv import load_dotenv

from app.ingest import ingest_policies

load_dotenv()

if __name__ == "__main__":
    count = ingest_policies()
    print(f"Ingested {count} chunks into Chroma.")
