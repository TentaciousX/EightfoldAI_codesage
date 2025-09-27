import sqlite3

# Database file path
DB_FILE = "codesage.db"  # will be created in backend root

def get_connection():
    """
    Returns a SQLite connection with dict-like row access.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS problems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        contest_id INTEGER,
        problem_index TEXT,
        name TEXT,
        rating INTEGER,
        tags TEXT
    )
    """)

    # Sessions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id TEXT,
        start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        end_time TIMESTAMP,
        current_problem_id INTEGER,
        difficulty_level TEXT
    )
    """)

    # Submissions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id TEXT,
        session_id INTEGER,
        problem_id INTEGER,
        code TEXT,
        language TEXT,
        execution_result TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Candidate state table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidate_state (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id INTEGER,
        progress_stage TEXT,
        errors TEXT,
        strategy_shift TEXT,
        confidence_level TEXT,
        clarity_level TEXT,
        thinking_aloud INTEGER,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized and tables created successfully!")
