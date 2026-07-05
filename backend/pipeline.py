"""
==========================================================
AccountaAI - Processing Pipeline
----------------------------------------------------------
Coordinates AI, Database, RAG and Reminder Engine
==========================================================
"""

from backend.ai import ai_engine
from backend.database import db
from backend.rag import rag
from backend.reminder import schedule_reminders


class Pipeline:

    def process(self, audio_path: str, meeting_title: str):

        # ------------------------------
        # AI Processing
        # ------------------------------

        result = ai_engine.process_meeting(audio_path)

        transcript = result["transcript"]
        analysis = result["analysis"]

        # ------------------------------
        # Store Meeting
        # ------------------------------

        meeting_id = db.add_meeting(
            title=meeting_title,
            meeting_date="Today",
            transcript=transcript,
            summary=analysis.summary,
            accountability_score=analysis.accountability_score
        )

        # ------------------------------
        # Store in RAG
        # ------------------------------

        rag.add_meeting(
            meeting_id,
            transcript
        )

        # ------------------------------
        # Save Tasks
        # ------------------------------

        for task in analysis.tasks:

            task_id = db.add_task(
                meeting_id,
                task.task,
                task.owner,
                task.deadline,
                task.priority,
                task.status
            )

            schedule_reminders(
                task_id=task_id,
                owner_email=task.owner,
                deadline=task.deadline,
                priority=task.priority,
                task_name=task.task
            )

        return {
            "meeting_id": meeting_id,
            "transcript": transcript,
            "analysis": analysis
        }


pipeline = Pipeline()