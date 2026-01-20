from functools import wraps
from flask import request


def paginate(default_page=1, default_per_page=10):
    """
    Decorator to extract pagination params from request
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            page = request.args.get("page", default_page, type=int)
            per_page = request.args.get("per_page", default_per_page, type=int)

            return func(page=page, per_page=per_page, *args, **kwargs)

        return wrapper

    return decorator
