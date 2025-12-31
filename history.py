"""
Chat session management with SQLite persistence.
Sessions (titles, metadata) stored in our table, messages stored via LangGraph checkpointer.
"""

import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass


# Database path (shared with graph.py checkpointer)
DB_PATH = Path("chat_history.db")


@dataclass
class ChatSession:
    """Represents a chat session."""
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    provider: str
    model: str


def get_db_connection() -> sqlite3.Connection:
    """Get a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initialize the database schema for sessions."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create sessions table (messages are stored by LangGraph checkpointer)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_sessions (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            provider TEXT,
            model TEXT
        )
    """)
    
    conn.commit()
    conn.close()


def create_session(provider: str = "", model: str = "") -> ChatSession:
    """Create a new chat session."""
    session_id = str(uuid.uuid4())
    now = datetime.now()
    title = "New Chat"
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO chat_sessions (id, title, created_at, updated_at, provider, model)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (session_id, title, now, now, provider, model)
    )
    conn.commit()
    conn.close()
    
    return ChatSession(
        id=session_id,
        title=title,
        created_at=now,
        updated_at=now,
        provider=provider,
        model=model
    )


def get_session(session_id: str) -> ChatSession | None:
    """Get a chat session by ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat_sessions WHERE id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return ChatSession(
            id=row["id"],
            title=row["title"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            provider=row["provider"] or "",
            model=row["model"] or ""
        )
    return None


def get_all_sessions() -> list[ChatSession]:
    """Get all chat sessions, ordered by most recent first."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat_sessions ORDER BY updated_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    sessions = []
    for row in rows:
        sessions.append(ChatSession(
            id=row["id"],
            title=row["title"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            provider=row["provider"] or "",
            model=row["model"] or ""
        ))
    return sessions


def update_session_title(session_id: str, title: str) -> None:
    """Update the title of a chat session."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE chat_sessions SET title = ?, updated_at = ? WHERE id = ?",
        (title, datetime.now(), session_id)
    )
    conn.commit()
    conn.close()


def update_session_timestamp(session_id: str) -> None:
    """Update the timestamp of a chat session."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE chat_sessions SET updated_at = ? WHERE id = ?",
        (datetime.now(), session_id)
    )
    conn.commit()
    conn.close()


def delete_session(session_id: str) -> None:
    """Delete a chat session."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_sessions WHERE id = ?", (session_id,))
    conn.commit()
    conn.close()


# Initialize database on module import
init_db()
