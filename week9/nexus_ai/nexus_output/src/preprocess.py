import re
from typing import Tuple

def redact_pii(text: str) -> str:
    """Simple PII redaction for emails and phone numbers.
    In production replace with a robust solution.
    """
    # redact emails
    text = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[REDACTED_EMAIL]", text)
    # redact phone numbers (basic patterns)
    text = re.sub(r"\+?\d[\d\s().-]{7,}\d", "[REDACTED_PHONE]", text)
    return text

def preprocess_document(content: str) -> str:
    """Run preprocessing steps on raw document content.
    Currently applies PII redaction and strips excessive whitespace.
    """
    clean = redact_pii(content)
    # normalize whitespace
    clean = "\n".join(line.strip() for line in clean.splitlines() if line.strip())
    return clean
