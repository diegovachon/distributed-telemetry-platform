import sqlite3


DATABASE_NAME = "telemetry.db"

def initialize_database():
    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hostname TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            cpu_percent REAL NOT NULL,
            memory_percent REAL NOT NULL,
            disk_percent REAL NOT NULL
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hostname TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        severity TEXT NOT NULL,
        message TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def insert_metric(metrics):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO telemetry (
            hostname,
            timestamp,
            cpu_percent,
            memory_percent,
            disk_percent
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            metrics["hostname"],
            metrics["timestamp"],
            metrics["cpu_percent"],
            metrics["memory_percent"],
            metrics["disk_percent"]
        )
    )

    connection.commit()
    connection.close()


def get_all_metrics():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            hostname,
            timestamp,
            cpu_percent,
            memory_percent,
            disk_percent
        FROM telemetry
    """)

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]

def get_latest_metric(hostname):
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            hostname,
            timestamp,
            cpu_percent,
            memory_percent,
            disk_percent
        FROM telemetry
        WHERE hostname = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (hostname,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    return dict(row)


def insert_alert(alert):
    connection = sqlite3.connect(DATABASE_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO alerts(
            hostname,
            timestamp,
            severity,
            message
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            alert["hostname"],
            alert["timestamp"],
            alert["severity"],
            alert["message"]
        )
    )

    connection.commit()
    connection.close()


def get_all_alerts():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            hostname,
            timestamp,
            severity,
            message
        FROM alerts
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return [dict(row) for row in rows]