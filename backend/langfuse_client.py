"""
==========================================================
AccountaAI - Langfuse Client
----------------------------------------------------------
Centralized Langfuse Initialization

Compatible with Langfuse v3

Used by:
• AI Engine
• Pipeline
• RAG
• Streamlit App
==========================================================
"""

from langfuse import get_client

from backend.config import (
    LANGFUSE_PUBLIC_KEY,
    LANGFUSE_SECRET_KEY,
    LANGFUSE_HOST,
)

# ==========================================================
# INITIALIZE LANGFUSE CLIENT
# ==========================================================

langfuse = get_client()

print("=" * 50)
print("Langfuse Client Initialized")
print(f"Host : {LANGFUSE_HOST}")
print("=" * 50)


# ==========================================================
# TRACE HELPERS
# ==========================================================

def start_trace(
    name: str,
    user_id: str = "anonymous",
    session_id: str = "default",
):
    """
    Starts a new root trace.

    Usage:
        with start_trace("Meeting Analysis") as trace:
            ...
    """

    return langfuse.start_as_current_span(
        name=name,
        input={
            "user_id": user_id,
            "session_id": session_id,
        },
    )


def start_span(
    name: str,
    input_data=None,
):
    """
    Starts a child span.

    Usage:
        with start_span("Whisper") as span:
            ...
    """

    return langfuse.start_as_current_span(
        name=name,
        input=input_data,
    )


# ==========================================================
# UPDATE HELPERS
# ==========================================================

def update_input(
    span,
    data,
):
    """
    Update span input.
    """

    try:
        span.update(input=data)
    except Exception:
        pass


def update_output(
    span,
    data,
):
    """
    Update span output.
    """

    try:
        span.update(output=data)
    except Exception:
        pass


def update_metadata(
    span,
    metadata: dict,
):
    """
    Add metadata to a span.
    """

    try:
        span.update(metadata=metadata)
    except Exception:
        pass


def update_status(
    span,
    status: str,
):
    """
    Add a status field.
    """

    try:
        span.update(metadata={"status": status})
    except Exception:
        pass


# ==========================================================
# ERROR LOGGING
# ==========================================================

def log_error(
    span,
    error: Exception,
):
    """
    Record exception details.
    """

    try:
        span.update(
            level="ERROR",
            status_message=str(error),
        )
    except Exception:
        pass


# ==========================================================
# FLUSH
# ==========================================================

def flush():
    """
    Flush pending events to Langfuse.
    """

    try:
        langfuse.flush()
    except Exception:
        pass