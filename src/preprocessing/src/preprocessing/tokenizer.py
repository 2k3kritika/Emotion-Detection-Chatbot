from typing import List


def tokenize(text: str) -> List[str]:
    """Simple whitespace tokenizer. Returns empty list on empty input."""
    if not text:
        return []
    return text.split()
