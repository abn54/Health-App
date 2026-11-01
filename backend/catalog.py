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


def normalized_question(text):
    return " ".join(unicodedata.normalize("NFKC", text).lower().replace("’", "'").split())


def scope_question(text):
    """Content boundary, not a clinical assessment. Never gates manual support."""
    text = normalized_question(text)
    return bool(re.search(
        r"\b(?:therapist|therapy|diagnos\w*|monitor(?:ing|ed)?|prescrib\w*|medicat\w*|dosage|dose|tablets?|pills?)\b"
        r"|\bdo i have\b.*\b(?:anxiety|depression|adhd|bpd|a disorder)\b", text))


def mock_reply(text):
    """Reviewed-topic routing for unrestricted wording; no emotion or risk scoring.

    Word boundaries prevent 'friend/weekend' from accidentally matching 'end'.
    Explicit feature questions precede everyday situations; clinical scope stays
    separate. A miss asks for clarification instead of repeating role warnings.
    """
    text = normalized_question(text)
    if scope_question(text):
        return "scope"
    groups = [
        ("about", r"\b(?:purpose|what is mello|what's mello|about mello|app for|mello help|app help|what is this app)\b"),
        ("checkin", r"\b(?:check[- ]in|questionnaire|clicks?)\b|\b(?:infer|detect|judge|track)\w*\b.*\b(?:mood|stress)\b"),
        ("preferences", r"\b(?:remember\w*|usual|preferences?|favorites?|favourites?)\b"),
        ("resources", r"\b(?:resources?|handbooks?|dsm|references?|reading shelf|sources?)\b"),
        ("stress", r"\b(?:what is stress|what stress is|define stress|stress means?)\b"),
        ("motion", r"\b(?:circle|motion|moving|shape|text[- ]only|animation)\b"),
        ("storage", r"\b(?:sav\w*|stor\w*|records?|history|data|delet\w*)\b|\bclose (?:this|the app|mello)\b"),
        ("choose_skill", r"\b(?:which|choose|choosing|prefer|compare|difference|another)\b.*\b(?:practices?|skills?|exercises?|one)\b|\bwhich one\b"),
        ("skills", r"\b(?:grounding|5[-–]4[-–]3|stop practice|stop exercise|exercises|available skills|other practice)\b"),
        ("controls", r"\b(?:pause|resume|halfway)\b|\b(?:stop|end|leave|exit)\b.*\b(?:exercise|practice|session|app|halfway)\b"),
        ("exam", r"\b(?:exams?|tests?|quiz(?:zes)?|midterms?|finals?|revis(?:ion|ing|e)|grades?|fail(?:ing|ure)?|presentations?|public speaking)\b"),
        ("rest", r"\b(?:sleep\w*|bed(?:time)?|insomnia|rest|tired|exhausted|wind(?:ing)? down|lying awake|at night)\b"),
        ("finding_support", r"\b(?:counsell?ing|counsell?or|professional help|seek help|find support|find help|someone to talk|need help|support team)\b|\bwhen (?:should|do) i\b.*\bhelp\b"),
        ("connection", r"\b(?:friends?|friendship|relationships?|roommates?|lonely|loneliness|alone|homesick|left out|breakup)\b"),
        ("study", r"\b(?:study\w*|studying|homework|coursework|workload|assignments?|deadlines?|focus|concentrat\w*|procrastinat\w*|tasks?|planning|plan)\b"),
        ("overwhelmed", r"\b(?:stress\w*|overwhelm\w*|worr\w*|anxious|anxiety|nervous|sad|low mood|too much|cope|coping|calm|tense|scared)\b"),
        ("pacing", r"\b(?:long|counts?|cycles?|pace|pacing|breath\w*|seconds?)\b"),
        ("start", r"\b(?:start|begin|question first)\b"),
        ("greeting", r"^(?:hi|hello|hey|thanks|thank you|can we talk)[!.?, ]*$"),
    ]
    return next((topic for topic, pattern in groups if re.search(pattern, text)), "unsupported")


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
