"""
Author: Amir Ghaffari
Assignment: #2
Description: Port Scanner — A tool that scans a target machine for open network ports
"""

import socket
import threading
import sqlite3
import os
import platform
import datetime

print("Python Version:", platform.python_version())
print("Operating System:", os.name)

# This dictionary stores common port numbers and their related service names.
common_ports = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP-Alt"
}


class NetworkTool:
    def __init__(self, target):
        self.__target = target

    # Q3: What is the benefit of using @property and @target.setter?
    # Using @property and @target.setter lets the program control how the target
    # value is read and changed without exposing the private variable directly.
    # This makes the code safer because validation can happen in one place.
    # It also keeps the class organized and easier to maintain later.
    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, value):
        if value != "":
            self.__target = value
        else:
            print("Error: Target cannot be empty")

    def __del__(self):
        print("NetworkTool instance destroyed")


# Q1: How does PortScanner reuse code from NetworkTool?
# PortScanner reuses code from NetworkTool by inheriting its target attribute,
# property methods, and validation logic instead of rewriting them again.
# For example, when PortScanner calls super().__init__(target), it uses the
# parent constructor to store the target as a private value.
class PortScanner(NetworkTool):
    def __init__(self, target):
        super().__init__(target)
        self.scan_results = []
        self.lock = threading.Lock()

    def __del__(self):
        print("PortScanner instance destroyed")
        super().__del__()

    def scan_port(self, port):
        sock = None
        # Q4: What would happen without try-except here?
        # Without try-except, any socket error such as an unreachable machine or
        # network problem could stop the whole program unexpectedly.
        # The scanner would crash instead of continuing with the remaining ports.
        # Exception handling makes the program more stable and user friendly.
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((self.target, port))

            if result == 0:
                status = "Open"
            else:
                status = "Closed"

            service_name = common_ports.get(port, "Unknown")

            self.lock.acquire()
            self.scan_results.append((port, status, service_name))
            self.lock.release()
        except socket.error as e:
            print(f"Error scanning port {port}: {e}")
        finally:
            if sock is not None:
                sock.close()

    def get_open_ports(self):
        return [result for result in self.scan_results if result[1] == "Open"]

    # Q2: Why do we use threading instead of scanning one port at a time?
    # Threading lets the scanner check many ports at the same time, which makes
    # the scan much faster than scanning one by one.
    # If 1024 ports were scanned without threads, the program could take a long
    # time because each port would wait for its timeout before moving on.
    def scan_range(self, start_port, end_port):
        threads = []

        for port in range(start_port, end_port + 1):
            thread = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(thread)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()


def save_results(target, results):
    conn = None
    try:
        conn = sqlite3.connect("scan_history.db")
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT,
                port INTEGER,
                status TEXT,
                service TEXT,
                scan_date TEXT
            )
            """
        )

        for port, status, service in results:
            cursor.execute(
                "INSERT INTO scans (target, port, status, service, scan_date) VALUES (?, ?, ?, ?, ?)",
                (target, port, status, service, str(datetime.datetime.now()))
            )

        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()


def load_past_scans():
    conn = None
    try:
        if not os.path.exists("scan_history.db"):
            print("No past scans found.")
            return

        conn = sqlite3.connect("scan_history.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM scans")
        rows = cursor.fetchall()

        if not rows:
            print("No past scans found.")
            return

        for row in rows:
            print(f"[{row[5]}] {row[1]} : Port {row[2]} ({row[4]}) - {row[3]}")
    except sqlite3.Error:
        print("No past scans found.")
    finally:
        if conn:
            conn.close()


# ============================================================
# MAIN PROGRAM
# ============================================================
if __name__ == "__main__":
    target = input("Enter target IP address (press Enter for 127.0.0.1): ").strip()
    if target == "":
        target = "127.0.0.1"

    try:
        start_port = int(input("Enter starting port number: "))
        end_port = int(input("Enter ending port number: "))

        if start_port < 1 or start_port > 1024 or end_port < 1 or end_port > 1024:
            print("Port must be between 1 and 1024.")
        elif end_port < start_port:
            print("Port must be between 1 and 1024.")
        else:
            scanner = PortScanner(target)
            print(f"Scanning {target} from port {start_port} to {end_port}...")
            scanner.scan_range(start_port, end_port)

            open_ports = scanner.get_open_ports()

            print(f"--- Scan Results for {target} ---")
            for port, status, service in open_ports:
                print(f"Port {port}: {status} ({service})")
            print("------")
            print(f"Total open ports found: {len(open_ports)}")

            save_results(target, scanner.scan_results)

            show_history = input("Would you like to see past scan history? (yes/no): ").strip().lower()
            if show_history == "yes":
                load_past_scans()
    except ValueError:
        print("Invalid input. Please enter a valid integer.")


# Q5: New Feature Proposal
# One extra feature I would add is a port risk classifier that labels open ports as high,
# medium, or low risk based on common security concerns. It could use a nested if-statement
# to check the port number and assign a risk level before printing the final report.
# Diagram: See diagram_studentID.png in the repository root
