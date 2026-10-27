"""Authored application facts, never therapy transcripts or generated advice."""
import re
import unicodedata
import json
from pathlib import Path

CONTENT = json.loads((Path(__file__).resolve().parents[1] / "shared/help-content.json").read_text())
VERSION = CONTENT["version"]
FALLBACK = "The optional explanation is unavailable. You can still start the exercise or open Crisis support."
BOUNDARY = "This prototype cannot respond to a crisis or connect you to a person. Crisis-support information is available here. Nobody monitors this app."
PHRASES = ("kill myself", "end my life", "hurt myself", "want to die")

# One reviewed source supplies both the browser FAQ and model-approved copy.
MODEL_CONTEXT = {key: value["context"] for key, value in CONTENT["topics"].items()}
CATALOG = {key: value["answer"] for key, value in CONTENT["topics"].items()}


def cue_match(text):
    normalized = " ".join(unicodedata.normalize("NFKC", text).lower().replace("’", "'").split())
    return any(re.search(r"(?<!\w)" + re.escape(p) + r"(?!\w)", normalized) for p in PHRASES)


def mock_reply(text):
    text = text.lower()
    groups = {
        "scope": ("therapist", "therapy", "diagnos", "monitor", "purpose"),
        "checkin": ("check-in", "check in", "questionnaire", "click", "mood"),
        "preferences": ("remember", "usual", "preference", "favorite", "favourite"),
        "resources": ("resource", "handbook", "dsm", "reference", "reading", "source"),
        "stress": ("what is stress", "what stress is", "define stress", "stress mean"),
        "motion": ("circle", "motion", "moving", "text only", "text-only", "animation"),
        "storage": ("sav", "stor", "record", "close", "history", "data", "delet"),
        "controls": ("stop", "pause", "resume", "end", "halfway"),
        "pacing": ("long", "count", "cycle", "pace", "pacing", "breath", "seconds"),
        "start": ("start", "begin", "question first"),
    }
    return next((key for key, words in groups.items() if any(w in text for w in words)), "unsupported")
