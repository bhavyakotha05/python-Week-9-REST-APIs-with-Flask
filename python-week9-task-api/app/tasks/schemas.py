from datetime import datetime


ALLOWED_STATUS = {"pending", "in_progress", "completed"}
ALLOWED_PRIORITY = {"low", "medium", "high"}


def validate_task_data(data, update=False):
    """
    Validate task payload.
    If update=True, fields are optional.
    """
    errors = {}

    if not update:
        if not data.get("title"):
            errors["title"] = "Title is required"
        elif len(data["title"]) < 3:
            errors["title"] = "Title must be at least 3 characters"

    if "status" in data and data["status"] not in ALLOWED_STATUS:
        errors["status"] = f"Status must be one of {list(ALLOWED_STATUS)}"

    if "priority" in data and data["priority"] not in ALLOWED_PRIORITY:
        errors["priority"] = f"Priority must be one of {list(ALLOWED_PRIORITY)}"

    if "due_date" in data:
        try:
            # Expect YYYY-MM-DD
            datetime.strptime(data["due_date"], "%Y-%m-%d")
        except ValueError:
            errors["due_date"] = "due_date must be in YYYY-MM-DD format"

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
