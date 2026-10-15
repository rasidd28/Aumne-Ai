import re
from typing import List, Tuple

# Restricted words and derogatory terms
BANNED_WORDS = [
    "damn", "hell", "crap", "ass", "bastard", "idiot", "moron", "stupid",
    "dumb", "loser", "jerk", "fool", "imbecile", "cretin", "dolt", "halfwit",
    "scumbag", "coward", "disgusting", "repulsive", "filth", "trash",
    "garbage", "worthless", "hate",
]

MIN_LENGTH = 50
MAX_LENGTH = 2000
CAPS_THRESHOLD = 0.6
CAPS_MIN_LETTERS = 8


def _check_length(content: str) -> List[str]:
    length = len(content.strip())
    if length < MIN_LENGTH:
        return [f"Content is too short. Minimum required length: {MIN_LENGTH} characters."]
    if length > MAX_LENGTH:
        return [f"Content is too long. Maximum allowed length: {MAX_LENGTH} characters."]
    return []


def _check_banned_words(title: str, content: str) -> List[str]:
    text = f"{title} {content}".lower()
    found = [w for w in BANNED_WORDS if re.search(rf"\b{re.escape(w)}\b", text)]
    if not found:
        return []
    return [
        f"Banned word(s) detected: {', '.join(found)}. "
        "Please remove inappropriate language."
    ]


def _check_tone(content: str) -> List[str]:
    reasons = []
    letters = [ch for ch in content if ch.isalpha()]

    if len(letters) >= CAPS_MIN_LETTERS:
        ratio = sum(ch.isupper() for ch in letters) / len(letters)
        if ratio > CAPS_THRESHOLD:
            reasons.append(
                f"Content sounds aggressive (all-caps, {ratio:.0%} uppercase). "
                "Please write in normal sentence case."
            )

    if re.search(r"[!?]{4,}", content):
        reasons.append(
            "Content has excessive punctuation (e.g. '!!!!'), which reads as aggressive."
        )

    return reasons


def moderate_content(title: str, content: str) -> Tuple[bool, List[str]]:
    """Return (approved, reasons). Every failed rule adds a reason."""
    reasons = (
        _check_length(content)
        + _check_banned_words(title, content)
        + _check_tone(content)
    )
    return (not reasons, reasons)
