"""
==========================================================
AccountaAI - AI Engine
----------------------------------------------------------
Handles:
1. Speech-to-Text (Whisper)
2. Video-to-Audio Conversion (FFmpeg)
3. Meeting Analysis (Gemini)
4. Pydantic Validation
==========================================================
"""

import json
import os

import ffmpeg
import whisper
import shutil

FFMPEG_PATH = shutil.which("ffmpeg")

from google import genai
from google.genai import types

from backend.config import (
    GOOGLE_API_KEY,
    GEMINI_MODEL,
    WHISPER_MODEL
)

from backend.prompts import MEETING_ANALYSIS_PROMPT
from backend.models import MeetingAnalysis
from backend.langfuse_client import langfuse

# ==========================================================
# VIDEO -> AUDIO
# ==========================================================
#FFMPEG_PATH = r"C:\Users\Yashwanth Boya\Downloads\ffmpeg-8.1.2-essentials_build\ffmpeg-8.1.2-essentials_build\bin\ffmpeg.exe"

def extract_audio(video_path: str) -> str:
    """
    Extract audio from a video file and convert it to 16kHz mono WAV.
    """

    audio_path = os.path.splitext(video_path)[0] + ".wav"

    (
        ffmpeg
        .input(video_path)
        .output(
            audio_path,
            ac=1,
            ar=16000
        )
        .overwrite_output()
        .run(
            cmd=FFMPEG_PATH if FFMPEG_PATH else "ffmpeg",
            quiet=True
        )
    )

    return audio_path


# ==========================================================
# AI ENGINE
# ==========================================================

class AIEngine:
    """
    Main AI Engine
    """

    def __init__(self):

        # Gemini Client
        self.client = genai.Client(
            api_key=GOOGLE_API_KEY
        )

        # Whisper Model
        print("=" * 50)
        print("Loading Whisper Model...")
        self.whisper_model = whisper.load_model(
            WHISPER_MODEL
        )
        print("Whisper Loaded Successfully!")
        print("=" * 50)

    # ------------------------------------------------------

    def transcribe_audio(self, file_path: str) -> str:
        """
        Converts audio/video into transcript.
        """

        VIDEO_EXTENSIONS = (
            ".mp4",
            ".mov",
            ".avi",
            ".mkv",
            ".webm"
        )

        if file_path.lower().endswith(VIDEO_EXTENSIONS):

            print("Video Detected")
            file_path = extract_audio(file_path)

        print("Transcribing Meeting...")

        result = self.whisper_model.transcribe(file_path)

        transcript = result["text"]

        print("Transcription Completed")

        return transcript

    # ------------------------------------------------------
    def analyze_meeting(
        self,
        transcript: str
    ) -> MeetingAnalysis:

        with langfuse.start_as_current_span(
            name="Meeting Analysis"
        ) as span:

            span.update(
                input={
                    "transcript": transcript
                }
            )

            prompt = f"""
            {MEETING_ANALYSIS_PROMPT}

            Meeting Transcript:

            {transcript}
            """

            response = self.client.models.generate_content(

                model=GEMINI_MODEL,

                contents=prompt,

                config=types.GenerateContentConfig(

                temperature=0.2,

                response_mime_type="application/json"

            )

        )

            span.update(
                output=response.text
            )

            ai_response = response.text

    

            try:

                data = json.loads(ai_response)

            except Exception:

                data = {
                    "summary": ai_response,
                    "decisions": [],
                    "tasks": [],
                    "accountability_score": 0
                }

            data.setdefault("summary", "")
            data.setdefault("decisions", [])
            data.setdefault("tasks", [])
            data.setdefault("accountability_score", 0)

            analysis = MeetingAnalysis.model_validate(
                data
            )

            return analysis

    # ------------------------------------------------------

    def process_meeting(
        self,
        file_path: str
    ):
        """
        Complete Meeting Processing Pipeline
        """

        transcript = self.transcribe_audio(
            file_path
        )

        analysis = self.analyze_meeting(
            transcript
        )

        return {

            "transcript": transcript,

            "analysis": analysis

        }


# ==========================================================
# INITIALIZE
# ==========================================================

ai_engine = AIEngine()
