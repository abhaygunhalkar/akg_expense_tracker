def clean_json_string(s: str) -> str:
    """Removes common markdown wrappers and surrounding text from a string."""
    s = s.strip()
    # Remove markdown code block fences
    if s.startswith("```json"):
        s = s[7:]
    if s.endswith("```"):
        s = s[:-3]
    s = s.strip()
    return s