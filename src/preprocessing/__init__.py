"""Public API for the preprocessing package.

This module supports being imported as a package (preferred) and
being executed directly as a script for quick checks. When run
directly Python does not set a parent package which makes relative
imports fail; we provide a fallback to import the same symbols using
an absolute import path after adding the project root to `sys.path`.
"""

try:
    from .text_cleaner import clean_text
    from .tokenizer import tokenize
    from .label_encoder import LabelEncoderWrapper
    from .preprocess_pipeline import preprocess_text
except Exception:
    import sys
    import os

    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    from src.preprocessing.text_cleaner import clean_text
    from src.preprocessing.tokenizer import tokenize
    from src.preprocessing.label_encoder import LabelEncoderWrapper
    from src.preprocessing.preprocess_pipeline import preprocess_text

__all__ = [
    "clean_text",
    "tokenize",
    "LabelEncoderWrapper",
    "preprocess_text",
]
