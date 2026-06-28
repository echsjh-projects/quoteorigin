"""
nlp/normalizer.py
-----------------
Normalizes a quote so that "Blood, sweat, and tears!" and
"blood sweat and tears" map to the same database record.
"""

import re
import unicodedata


def normalize_quote(text: str) -> str:
    """
    Canonical form used as the database lookup key.
    - Lowercase
    - Remove punctuation (except apostrophes in contractions)
    - Collapse whitespace
    - Strip leading/trailing whitespace
    - Normalize unicode (e.g. curly quotes → straight quotes)
    """
    # Normalize unicode: convert é → e, " → ", etc.
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")

    text = text.lower()

    # Remove punctuation except apostrophes (don't → dont would change meaning)
    text = re.sub(r"[^\w\s']", " ", text)

    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text
