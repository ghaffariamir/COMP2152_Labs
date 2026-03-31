import sqlite3
import unittest

DB_NAME = "audit.db"


def setup_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event TEXT,
            severity TEXT,
            timestamp TEXT
        )
    """)

    cursor.execute("DELETE FROM audit_log")

    data = [
        ("Login failed", "HIGH"),
        ("Access denied", "HIGH"),
        ("Malware detected", "HIGH"),
        ("User login", "LOW"),
        ("File opened", "LOW"),
        ("Settings changed", "MEDIUM"),
        ("Password updated", "MEDIUM"),
    ]

    for event, severity in data:
        cursor.execute(
            "INSERT INTO audit_log (event, severity, timestamp) VALUES (?, ?, datetime('now'))",
            (event, severity)
        )

    conn.commit()
    conn.close()


def get_events_by_severity(severity):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM audit_log WHERE severity = ?", (severity,))
    rows = cursor.fetchall()

    conn.close()
    return rows


def get_recent_events(limit):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM audit_log ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )
    rows = cursor.fetchall()

    conn.close()
    return rows


def count_by_severity():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT severity, COUNT(*)
        FROM audit_log
        GROUP BY severity
        ORDER BY COUNT(*) DESC
    """)
    rows = cursor.fetchall()

    conn.close()
    return rows


def safe_query(query):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()


class TestAuditLog(unittest.TestCase):

    def test_high_severity(self):
        rows = get_events_by_severity("HIGH")
        self.assertEqual(len(rows), 3)

    def test_recent_events(self):
        rows = get_recent_events(5)
        self.assertEqual(len(rows), 5)

    def test_count(self):
        results = count_by_severity()
        self.assertIn(("HIGH", 3), results)

    def test_safe_bad_query(self):
        result = safe_query("SELECT * FROM fake_table")
        self.assertEqual(result, [])


if __name__ == "__main__":
    setup_db()

    print("\n--- Running Unit Tests ---")
    unittest.main()