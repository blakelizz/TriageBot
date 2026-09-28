PROMPT_INJECTION_PATTERNS = {
    "ignore tes instructions",
    "ignore previous instructions",
    "system prompt",
    "mode dev",
    "please ignore",
    "override",
}

def is_prompt_injection(message: str) -> bool:
    msg = message.lower()
    return any(pattern in msg for pattern in PROMPT_INJECTION_PATTERNS)
