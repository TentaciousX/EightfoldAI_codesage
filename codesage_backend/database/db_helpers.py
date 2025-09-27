from database.db import get_connection

# ----------------------------
# Problems helpers
# ----------------------------
def insert_problem(contest_id, problem_index, name, rating, tags):
    """
    Insert a problem into the problems table.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO problems (contest_id, problem_index, name, rating, tags)
        VALUES (?, ?, ?, ?, ?)
    """, (contest_id, problem_index, name, rating, tags))
    conn.commit()
    conn.close()

def get_problem_by_id(problem_id):
    """
    Fetch a problem by its ID.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM problems WHERE id = ?", (problem_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def get_problems_by_rating(min_rating=0, max_rating=5000):
    """
    Fetch problems by rating directly.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM problems
        WHERE rating BETWEEN ? AND ?
    """, (min_rating, max_rating))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ----------------------------
# Sessions helpers
# ----------------------------
def create_session(candidate_id, current_problem_id=None):
    """
    Create a new session for a candidate. Optionally set the current problem.
    Returns session_id.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO sessions (candidate_id, current_problem_id)
        VALUES (?, ?)
    """, (candidate_id, current_problem_id))
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id

def get_session(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# ----------------------------
# Submissions helpers
# ----------------------------
def insert_submission(candidate_id, session_id, problem_id, code, language, execution_result):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO submissions (candidate_id, session_id, problem_id, code, language, execution_result)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (candidate_id, session_id, problem_id, code, language, execution_result))
    conn.commit()
    conn.close()

def get_submissions_for_session(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM submissions WHERE session_id = ?", (session_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ----------------------------
# Candidate state helpers
# ----------------------------
def create_candidate_state(session_id, progress_stage="not_started", errors="", strategy_shift="none",
                           confidence_level="medium", clarity_level="clear", thinking_aloud=0):
    """
    Initialize candidate state for a session.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO candidate_state (session_id, progress_stage, errors, strategy_shift,
                                     confidence_level, clarity_level, thinking_aloud)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (session_id, progress_stage, errors, strategy_shift, confidence_level, clarity_level, thinking_aloud))
    conn.commit()
    conn.close()

def update_candidate_state(session_id, **kwargs):
    """
    Update candidate state fields for a session.
    Acceptable kwargs: progress_stage, errors, strategy_shift, confidence_level, clarity_level, thinking_aloud
    """
    if not kwargs:
        return

    conn = get_connection()
    cursor = conn.cursor()

    fields = []
    values = []
    for key, val in kwargs.items():
        fields.append(f"{key} = ?")
        values.append(val)
    values.append(session_id)

    cursor.execute(f"""
        UPDATE candidate_state
        SET {', '.join(fields)}, last_updated = CURRENT_TIMESTAMP
        WHERE session_id = ?
    """, tuple(values))

    conn.commit()
    conn.close()

def get_candidate_state(session_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidate_state WHERE session_id = ?", (session_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
