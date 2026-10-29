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
        "scope": ("therapist", "therapy", "diagnos", "monitor"),
        "about": ("purpose", "what is mello", "what\'s mello", "about mello", "app for", "mello help", "app help", "what is this app"),
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


def compose_reply(reply_id, profile, current_cue):
    """Select reviewed copy from explicit profile/factual history; never ask a model to infer state."""
    topic = CONTENT["topics"][reply_id]
    answer = topic["brief"] if profile["reply_detail"] == "brief" else topic["answer"]
    context = {"reply_detail": profile["reply_detail"], "history_used": False}
    if not profile["use_history"] or reply_id not in {"start", "motion", "preferences", "controls", "pacing"}:
        return answer, context
    copy = CONTENT["personalization"]
    parts = [answer, copy["current"][current_cue]]
    context.update(history_used=True, current_cue=current_cue, remembered_cue=profile["remembered_cue"], latest_practice=profile["latest_practice"])
    remembered = profile["remembered_cue"]
    if remembered and remembered != current_cue:
        parts.append(copy["remembered"][remembered])
    latest = profile["latest_practice"]
    if latest:
        parts.append(copy["last_status"][latest["status"]])
        if latest["cue"] in copy["last_cue"]:
            parts.append(copy["last_cue"][latest["cue"]])
    else:
        parts.append(copy["none"])
    return " ".join(parts), context
