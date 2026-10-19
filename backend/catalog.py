"""Authored application facts, never therapy transcripts or generated advice."""
import re
import unicodedata

VERSION = "app-help-v1"
# Short factual index supplied as grounded model context. Full displayed copy below
# stays server-owned; selection needs distinctions, not long repetitive responses.
MODEL_CONTEXT = {
    "pacing": "Six cycles: inhale four one-second counts, exhale six. Total planned duration 60 seconds.",
    "motion": "Animated circle is optional. Text only shows words and counts. Cue changes preserve pace.",
    "storage": "SQLite saves questions, replies and session history locally. Check save status. Saved history is reviewable and deletable.",
    "controls": "Pause holds your place. Resume continues. End stops halfway immediately. Opening support pauses.",
    "scope": "Fictional coursework prototype only. No therapy, diagnosis or human monitoring.",
    "start": "Start begins the exercise from Ready. Answering a question first is optional.",
    "unsupported": "Personal mental-health advice or unrelated requests are outside the app-help scope.",
}
CATALOG = {
    "pacing": "The exercise has six cycles. Each cycle uses four one-second counts for inhale and six for exhale, for 60 seconds of planned pacing.",
    "motion": "You can choose Text only before or during the exercise. The inhale/exhale words and count still show the pace. Changing the cue does not restart pacing or save a remembered preference.",
    "storage": "The app attempts to save fictional questions, displayed replies, and session records in local SQLite. Check the save status; a failed save is not a stored record. Delete sessions and their conversations in History. Live mode sends the current question and limited context to the local Ollama model.",
    "controls": "Pause holds the current phase and count. Resume continues them. End stops the exercise. Crisis support stays available, and opening it pauses an active exercise.",
    "scope": "This coursework prototype demonstrates one prescribed skill and its interface. It does not provide therapy, diagnosis, or human monitoring. Use fictional scenarios only.",
    "start": "The ready screen shows the 60-second exercise and your cue setting. Start is your choice. You do not need to answer questions first.",
    "unsupported": "I can explain the pacing, controls, cue settings, and saved records. This prototype cannot advise on personal mental health concerns. Crisis-support information is available from the Crisis support control.",
}
FALLBACK = "The optional explanation is unavailable. You can still start the exercise or open Crisis support."
BOUNDARY = "This prototype cannot respond to a crisis or connect you to a person. Crisis-support information is available here. Nobody monitors this app."
PHRASES = ("kill myself", "end my life", "hurt myself", "want to die")


def cue_match(text):
    normalized = " ".join(unicodedata.normalize("NFKC", text).lower().replace("’", "'").split())
    return any(re.search(r"(?<!\w)" + re.escape(p) + r"(?!\w)", normalized) for p in PHRASES)


def mock_reply(text):
    text = text.lower()
    groups = {
        "motion": ("circle", "motion", "moving", "text only", "text-only", "animation"),
        "storage": ("sav", "stor", "record", "close", "history", "data", "delet"),
        "controls": ("stop", "pause", "resume", "end", "halfway"),
        "pacing": ("long", "count", "cycle", "pace", "pacing", "breath", "seconds"),
        "scope": ("therapy", "diagnos", "monitor", "purpose"),
        "start": ("start", "begin", "question first"),
    }
    return next((key for key, words in groups.items() if any(w in text for w in words)), "unsupported")
