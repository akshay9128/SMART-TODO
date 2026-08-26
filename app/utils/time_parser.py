from datetime import datetime


def parse_reminder_time(time_text: str) -> str:
    time_text = time_text.strip().lower()

    formats = [
        "%H:%M",
        "%I:%M %p",
        "%I %p",
        "%I:%M%p",
        "%I%p",
    ]

    for fmt in formats:
        try:
            parsed_time = datetime.strptime(time_text, fmt)
            return parsed_time.strftime("%H:%M")
        except ValueError:
            continue

    raise ValueError(
        "Invalid reminder time. Use formats such as 7 PM, 7:00 PM, or 19:00."
    )