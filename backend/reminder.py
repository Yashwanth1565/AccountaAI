from datetime import datetime

import resend
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import SchedulerAlreadyRunningError

from backend.config import RESEND_API_KEY
from backend.database import db

resend.api_key = RESEND_API_KEY

scheduler = BackgroundScheduler()


def send_email(
    recipient,
    task,
    deadline,
    priority
):

    try:

        resend.Emails.send({

            "from": "AccountaAI <onboarding@resend.dev>",

            "to": recipient,

            "subject": f"Reminder: {task}",

            "html": f"""

            <h2>Reminder</h2>

            <p><b>Task:</b> {task}</p>

            <p><b>Deadline:</b> {deadline}</p>

            <p><b>Priority:</b> {priority}</p>

            """

        })

        print("Reminder sent.")

    except Exception as e:

        print(e)


def schedule_reminders(
    task_id,
    owner_email,
    deadline,
    priority,
    task_name="Meeting Task"
):

    if owner_email and "@" in owner_email:

        db.add_reminder(
            task_id,
            owner_email,
            deadline
        )


def check_due_reminders():

    reminders = db.get_due_reminders()

    for reminder in reminders:

        send_email(

            reminder["email"],

            reminder["task"],

            reminder["reminder_date"],

            reminder["priority"]

        )

        db.mark_reminder_sent(
            reminder["id"]
        )


def start_scheduler():
    """Start the reminder scheduler exactly once."""

    # Don't add duplicate jobs
    if scheduler.get_job("meeting_reminders") is None:
        scheduler.add_job(
            check_due_reminders,
            trigger="interval",
            minutes=1,
            id="meeting_reminders",
            replace_existing=True,
        )

    # Don't start an already-running scheduler
    try:
        if not scheduler.running:
            scheduler.start()
            print("=" * 50)
            print("Reminder Scheduler Started")
            print("=" * 50)
    except SchedulerAlreadyRunningError:
        pass
