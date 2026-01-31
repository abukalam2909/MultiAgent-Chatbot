import os
from pathlib import Path

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("MYSQL_HOST", "localhost")
PORT = int(os.getenv("MYSQL_PORT", "3306"))
USER = os.getenv("MYSQL_USER", "")
PASSWORD = os.getenv("MYSQL_PASSWORD", "")
DB = os.getenv("MYSQL_DB", "structured_DB")

SCHEMA_PATH = Path("data/sql/schema.sql")
SEED_PATH = Path("data/sql/seed.sql")


def _exec_sql_file(cursor, path: Path) -> None:
    sql = path.read_text()
    for statement in [s.strip() for s in sql.split(";") if s.strip()]:
        cursor.execute(statement)


def main() -> None:
    conn = mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASSWORD,
    )
    conn.autocommit = True
    cursor = conn.cursor()

    _exec_sql_file(cursor, SCHEMA_PATH)

    cursor.execute(f"USE {DB}")
    _exec_sql_file(cursor, SEED_PATH)

    cursor.close()
    conn.close()
    print("Database initialized and seeded.")


if __name__ == "__main__":
    main()
