import re
from typing import Optional


def clean_text(text: Optional[str]) -> str:
    """Clean a single text string: lowercasing, remove punctuation, collapse spaces.

    Returns empty string for None or all-empty input.
    """
    if text is None:
        return ""
    text = str(text)
    text = text.strip()
    if not text:
        return ""
    text = text.lower()
    # remove punctuation
    text = re.sub(r"[^\w\s]", " ", text)
    # collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text
