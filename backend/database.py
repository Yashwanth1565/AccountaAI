"""
==========================================================
AccountaAI Database Layer
----------------------------------------------------------
Handles all SQLite operations.
==========================================================
"""

import sqlite3
from typing import List, Dict, Any

from backend.config import DATABASE_PATH


class DatabaseManager:
    """
    SQLite Database Manager
    """

    def __init__(self):
        self.connection = sqlite3.connect(
            DATABASE_PATH,
            check_same_thread=False
        )

        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

        self.create_tables()

    # -----------------------------------------------------

    def create_tables(self):

        # -----------------------------
        # Users
        # -----------------------------

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            email TEXT UNIQUE

        )
        """)

        # -----------------------------
        # Meetings
        # -----------------------------

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS meetings(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT,

            meeting_date TEXT,

            transcript TEXT,

            summary TEXT,

            accountability_score INTEGER

        )
        """)

        # -----------------------------
        # Tasks
        # -----------------------------

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            meeting_id INTEGER,

            task TEXT,

            owner TEXT,

            deadline TEXT,

            priority TEXT,

            status TEXT

        )
        """)

        # -----------------------------
        # Reminders
        # -----------------------------

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            task_id INTEGER,

            email TEXT,

            reminder_date TEXT,

            sent INTEGER DEFAULT 0

        )
        """)

        self.connection.commit()

    # =====================================================
    # USERS
    # =====================================================

    def add_user(self, name: str, email: str):

        self.cursor.execute(
            """
            INSERT OR IGNORE INTO users(name,email)
            VALUES(?,?)
            """,
            (name, email)
        )

        self.connection.commit()

    # =====================================================
    # MEETINGS
    # =====================================================

    def add_meeting(
        self,
        title: str,
        meeting_date: str,
        transcript: str,
        summary: str,
        accountability_score: int
    ):

        self.cursor.execute(
            """
            INSERT INTO meetings
            (
                title,
                meeting_date,
                transcript,
                summary,
                accountability_score
            )
            VALUES(?,?,?,?,?)
            """,
            (
                title,
                meeting_date,
                transcript,
                summary,
                accountability_score
            )
        )

        self.connection.commit()

        return self.cursor.lastrowid

    # =====================================================
    # TASKS
    # =====================================================

    def add_task(
        self,
        meeting_id,
        task,
        owner,
        deadline,
        priority,
        status
    ):

        self.cursor.execute(
            """
            INSERT INTO tasks
            (
                meeting_id,
                task,
                owner,
                deadline,
                priority,
                status
            )
            VALUES(?,?,?,?,?,?)
            """,
            (
                meeting_id,
                task,
                owner,
                deadline,
                priority,
                status
            )
        )

        self.connection.commit()

        return self.cursor.lastrowid

    # =====================================================
    # REMINDERS
    # =====================================================

    def add_reminder(
        self,
        task_id,
        email,
        reminder_date
    ):

        self.cursor.execute(
            """
            INSERT INTO reminders
            (
                task_id,
                email,
                reminder_date
            )
            VALUES(?,?,?)
            """,
            (
                task_id,
                email,
                reminder_date
            )
        )

        self.connection.commit()

    # =====================================================
    # FETCH DATA
    # =====================================================

    def get_all_meetings(self) -> List[Dict[str, Any]]:

        self.cursor.execute("""
        SELECT * FROM meetings
        ORDER BY id DESC
        """)

        rows = self.cursor.fetchall()

        return [dict(row) for row in rows]

    # -----------------------------------------------------

    def get_all_tasks(self):

        self.cursor.execute("""
        SELECT * FROM tasks
        """)

        rows = self.cursor.fetchall()

        return [dict(row) for row in rows]

    # -----------------------------------------------------

   # =====================================================
# REMINDER HELPERS
# =====================================================

    def get_due_reminders(self):

        self.cursor.execute("""
        SELECT
            reminders.id,
            reminders.task_id,
            reminders.email,
            reminders.reminder_date,
            tasks.task,
            tasks.priority
        FROM reminders
        JOIN tasks
        ON reminders.task_id = tasks.id
        WHERE reminders.sent = 0
        AND datetime(reminders.reminder_date) <= datetime('now')
        """)

        rows = self.cursor.fetchall()

        return [dict(row) for row in rows]


    def mark_reminder_sent(self, reminder_id):

        self.cursor.execute(
            """
            UPDATE reminders
            SET sent = 1
            WHERE id = ?
            """,
            (reminder_id,)
        )

        self.connection.commit()

db = DatabaseManager()