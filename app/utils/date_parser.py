from datetime import datetime, timedelta
import re


def parse_due_date(
    due_date: str | None,
    due_time: str | None = None
) -> datetime | None:

    if not due_date:
        return None

    due_date = due_date.lower().strip()

    now = datetime.now()

    # ---------------------------------
    # Determine target date
    # ---------------------------------

    if due_date == "today":

        target_date = now.date()

    elif due_date == "tomorrow":

        target_date = (now + timedelta(days=1)).date()

    else:

        weekdays = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6,
        }

        if due_date not in weekdays:
            return None

        target_day = weekdays[due_date]
        current_day = now.weekday()

        days_ahead = (target_day - current_day) % 7

        if days_ahead == 0:
            days_ahead = 7

        target_date = (
            now + timedelta(days=days_ahead)
        ).date()

    # ---------------------------------
    # Determine target time
    # ---------------------------------

    if due_time:

        due_time = due_time.lower().strip()

        match = re.match(
            r"^(\d{1,2})(?::(\d{2}))?\s*(am|pm)?$",
            due_time
        )

        if match:

            hour = int(match.group(1))
            minute = int(match.group(2) or 0)
            period = match.group(3)

            # 12-hour format
            if period == "pm" and hour != 12:
                hour += 12

            elif period == "am" and hour == 12:
                hour = 0

            # Validate time
            if hour < 0 or hour > 23:
                return None

            if minute < 0 or minute > 59:
                return None

            return datetime(
                target_date.year,
                target_date.month,
                target_date.day,
                hour,
                minute
            )

    # ---------------------------------
    # No time supplied
    # ---------------------------------

    return datetime.combine(
        target_date,
        now.time()
    )