import sqlite3

DB_NAME = "vault.db"


def setup_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT,
            username TEXT,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_credential(website, username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO vault (website, username, password) VALUES (?, ?, ?)",
        (website, username, password)
    )

    conn.commit()
    conn.close()


def get_all_credentials():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vault ORDER BY website ASC")
    rows = cursor.fetchall()

    conn.close()
    return rows


def find_credential(website):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM vault WHERE website = ?", (website,))
    rows = cursor.fetchall()

    conn.close()
    return rows


def display(rows):
    if not rows:
        print("  (no results)")
        return
    for row in rows:
        print(f"  {row[1]:<14} | {row[2]:<12} | {row[3]}")


if __name__ == "__main__":
    setup_db()

    print("\n" + "=" * 60)
    print("  PASSWORD VAULT")
    print("=" * 60)

    print("\n--- Adding Credentials ---")
    add_credential("github.com", "admin", "s3cur3P@ss")
    print("  Saved: github.com")

    add_credential("google.com", "maziar@gmail", "MyP@ssw0rd")
    print("  Saved: google.com")

    add_credential("netflix.com", "maziar", "N3tfl1x!")
    print("  Saved: netflix.com")

    add_credential("github.com", "work_user", "W0rkP@ss!")
    print("  Saved: github.com (work)")

    print("\n--- All Credentials ---")
    display(get_all_credentials())

    print("\n--- Search for 'github.com' ---")
    display(find_credential("github.com"))

    print("\n--- Search for 'spotify.com' ---")
    display(find_credential("spotify.com"))

    print("\n" + "=" * 60)