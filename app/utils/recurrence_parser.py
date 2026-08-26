import re


def parse_recurrence(text: str) -> tuple[str | None, str | None]:
    
    # Detect recurring patterns from natural language.like ex.users

    # Returns:
        # (recurrence_type, recurrence_value)
    

    text = text.lower().strip()

    # Every day
    if re.search(r"\bevery\s+day\b|\beveryday\b|\bdaily\b", text):
        return "daily", None

    # Every week
    if re.search(r"\bevery\s+week\b|\bweekly\b", text):
        return "weekly", None


    weekdays = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    for day in weekdays:
        if re.search(rf"\bevery\s+{day}\b", text):
            return "weekly", day

    if re.search(r"\bevery\s+month\b|\bmonthly\b", text):
        return "monthly", None

    return None, None