import re


def validate_registration_data(data):
    errors = {}

    if not data.get("username"):
        errors["username"] = "Username is required"

    if not data.get("email"):
        errors["email"] = "Email is required"
    elif not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
        errors["email"] = "Invalid email format"

    if not data.get("password"):
        errors["password"] = "Password is required"
    elif len(data["password"]) < 6:
        errors["password"] = "Password must be at least 6 characters"

    return errors
