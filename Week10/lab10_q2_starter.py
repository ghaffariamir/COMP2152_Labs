import sqlite3

DB_NAME = "login_tracker.db"


def setup_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            success BOOLEAN,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def record_attempt(username, success):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO login_attempts (username, success, timestamp) VALUES (?, ?, datetime('now'))",
        (username, success)
    )

    conn.commit()
    conn.close()


def get_failed_attempts(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM login_attempts WHERE username = ? AND success = 0",
        (username,)
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


def count_failures_per_user():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, COUNT(*)
        FROM login_attempts
        WHERE success = 0
        GROUP BY username
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def delete_old_attempts(username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM login_attempts WHERE username = ?",
        (username,)
    )

    deleted = cursor.rowcount

    conn.commit()
    conn.close()
    return deleted


def display_attempts(rows):
    for row in rows:
        status = "FAILED" if row[2] == 0 else "SUCCESS"
        print(f"  {row[1]:<8} | {status:<7} | {row[3]}")


def display_counts(rows):
    for row in rows:
        print(f"  {row[0]:<10} {row[1]} failed attempts")


if __name__ == "__main__":
    setup_db()

    print("\n" + "="*60)
    print("  LOGIN ATTEMPT TRACKER")
    print("="*60)

    print("\n--- Recording Login Attempts ---")
    record_attempt("admin", True)
    record_attempt("admin", False)
    record_attempt("admin", False)
    record_attempt("admin", False)
    record_attempt("guest", True)
    record_attempt("guest", False)
    record_attempt("root", False)
    record_attempt("root", False)
    record_attempt("root", False)
    record_attempt("root", False)

    print("\n--- Failed Attempts for 'admin' ---")
    display_attempts(get_failed_attempts("admin"))

    print("\n--- Failure Counts ---")
    display_counts(count_failures_per_user())

    print("\n--- Reset 'root' account ---")
    deleted = delete_old_attempts("root")
    print(f"  Deleted {deleted} records for root")

    print("\n--- Failure Counts (after reset) ---")
    display_counts(count_failures_per_user())

    print("\n" + "="*60)