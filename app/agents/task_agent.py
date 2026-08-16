import re


class TaskAgent:

    def process(self, text: str) -> dict:

        original_text = text
        text = text.lower().strip()

        text = re.sub(r"\ba\s*\.?\s*m\.?\b", "am", text)
        text = re.sub(r"\bp\s*\.?\s*m\.?\b", "pm", text)
        # INTENT DETECTION
        

        if any(word in text.split() for word in ["create", "add", "make"]):
            intent = "create_task"

        elif any(word in text.split() for word in ["delete", "remove"]):
            intent = "delete_task"

        elif any(word in text.split() for word in ["complete", "finish", "done"]):
            intent = "complete_task"

        elif any(word in text.split() for word in ["update", "change", "rename", "edit"]):
            intent = "update_task"

        elif any(word in text.split() for word in ["show", "list", "display"]):
            intent = "list_tasks"

        else:
            intent = "unknown"

        
        # EXTRACT TASK ID
        

        task_id = None

        match = re.search(
            r"\btask\s+(?:number\s+)?(\d+)\b",
            text
        )

        if match:
            task_id = int(match.group(1))

        else:
            match = re.search(r"#(\d+)", text)

            if match:
                task_id = int(match.group(1))

       
        # EXTRACT PRIORITY
       

        priority = None

        priority_match = re.search(
            r"\b(low|medium|high)\s+priority\b",
            text
        )

        if priority_match:
            priority = priority_match.group(1)

        
        # EXTRACT CATEGORY
        

        category = None

        category_match = re.search(
            r"\b(work|personal|study|health)\s+(?:task|item)\b",
            text
        )

        if category_match:
            category = category_match.group(1)

        
        # EXTRACT DUE DATE
        

        due_date = None

        if "today" in text:
            due_date = "today"

        elif "tomorrow" in text:
            due_date = "tomorrow"

        elif "monday" in text:
            due_date = "monday"

        elif "tuesday" in text:
            due_date = "tuesday"

        elif "wednesday" in text:
            due_date = "wednesday"

        elif "thursday" in text:
            due_date = "thursday"

        elif "friday" in text:
            due_date = "friday"

        elif "saturday" in text:
            due_date = "saturday"

        elif "sunday" in text:
            due_date = "sunday"

        
        # EXTRACT DUE TIME
        

        due_time = None

        time_match = re.search(
            r"\b("
            r"\d{1,2}:\d{2}\s*(?:am|pm)?"
            r"|"
            r"\d{1,2}\s*(?:am|pm)"
            r")\b",
            text
        )

        if time_match:
            due_time = time_match.group(1).strip()

        
        # EXTRACT TASK TITLE
        

        task_title = None

        # CREATE TASK
        if intent == "create_task":

            match = re.search(
                r"(?:create|add|make)"
                r"(?:\s+(?:a|an))?"
                r"(?:\s+(?:low|medium|high)\s+priority)?"
                r"(?:\s+(?:work|personal|study|health))?"
                r"\s+task"
                r"(?:\s+to)?\s+(.+)",
                text
            )

            if match:

                task_title = match.group(1).strip()

                # Remove priority phrase if it appears
                if priority:

                    task_title = re.sub(
                        r"\s+(?:with\s+)?"
                        r"(?:low|medium|high)\s+priority\b",
                        "",
                        task_title
                    ).strip()

                # Remove due time
                if due_time:

                    task_title = re.sub(
                        r"\s+(?:at\s+)?"
                        r"\d{1,2}:\d{2}\s*(?:am|pm)?\b",
                        "",
                        task_title
                    ).strip()

                    task_title = re.sub(
                        r"\s+(?:at\s+)?"
                        r"\d{1,2}\s*(?:am|pm)\b",
                        "",
                        task_title
                    ).strip()

                # Remove due date
                if due_date:

                    task_title = re.sub(
                        r"\s+(?:today|tomorrow)\b",
                        "",
                        task_title
                    ).strip()

                    task_title = re.sub(
                        r"\s+(?:on|by)\s+"
                        r"(?:monday|tuesday|wednesday|thursday|"
                        r"friday|saturday|sunday)\b",
                        "",
                        task_title
                    ).strip()

        # UPDATE TASK
        elif intent == "update_task":

            match = re.search(
                r"update\s+task\s+\d+\s+to\s+(.+)",
                text
            )

            if match:

                task_title = match.group(1).strip()

                # Remove priority phrase
                if priority:

                    task_title = re.sub(
                        r"\s+(?:with\s+)?"
                        r"(?:low|medium|high)\s+priority\b",
                        "",
                        task_title
                    ).strip()

                # Remove due time
                if due_time:

                    task_title = re.sub(
                        r"\s+(?:at\s+)?"
                        r"\d{1,2}:\d{2}\s*(?:am|pm)?\b",
                        "",
                        task_title
                    ).strip()

                    task_title = re.sub(
                        r"\s+(?:at\s+)?"
                        r"\d{1,2}\s*(?:am|pm)\b",
                        "",
                        task_title
                    ).strip()

                # Remove due date
                if due_date:

                    task_title = re.sub(
                        r"\s+(?:today|tomorrow)\b",
                        "",
                        task_title
                    ).strip()

                    task_title = re.sub(
                        r"\s+(?:on|by)\s+"
                        r"(?:monday|tuesday|wednesday|thursday|"
                        r"friday|saturday|sunday)\b",
                        "",
                        task_title
                    ).strip()

# FINAL RESULT


        return {
            "input": original_text,
            "intent": intent,
            "task_id": task_id,
            "task_title": task_title,
            "priority": priority,
            "category": category,
            "due_date": due_date,
            "due_time": due_time
        }