import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "prototype.db"


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


def initialize_database():
    connection = get_connection()

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS screenings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            document_text TEXT NOT NULL,
            importer TEXT,
            product TEXT,
            declared_value TEXT,
            hs_code TEXT,
            country_of_origin TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            screening_id INTEGER NOT NULL,
            rule_id TEXT NOT NULL,
            rule_status TEXT NOT NULL,
            explanation TEXT NOT NULL,
            reviewer_decision TEXT,
            reviewer_note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (screening_id) REFERENCES screenings(id)
        );
        """
    )

    connection.commit()
    connection.close()


def save_screening(document_text, fields):
    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO screenings (
            document_text,
            importer,
            product,
            declared_value,
            hs_code,
            country_of_origin
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            document_text,
            fields.get("importer"),
            fields.get("product"),
            fields.get("declared_value"),
            fields.get("hs_code"),
            fields.get("country_of_origin"),
        ),
    )

    screening_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return screening_id


def save_rule_results(screening_id, rule_results):
    connection = get_connection()
    saved_results = []

    for result in rule_results:
        cursor = connection.execute(
            """
            INSERT INTO audit_log (
                screening_id,
                rule_id,
                rule_status,
                explanation
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                screening_id,
                result["rule_id"],
                result["status"],
                result["explanation"],
            ),
        )

        saved_result = dict(result)
        saved_result["audit_id"] = cursor.lastrowid
        saved_results.append(saved_result)

    connection.commit()
    connection.close()

    return saved_results


def save_reviewer_decision(audit_id, decision, note):
    connection = get_connection()

    connection.execute(
        """
        UPDATE audit_log
        SET reviewer_decision = ?,
            reviewer_note = ?
        WHERE id = ?
        """,
        (
            decision,
            note,
            audit_id,
        ),
    )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print(f"Database initialized at: {DATABASE_PATH}")