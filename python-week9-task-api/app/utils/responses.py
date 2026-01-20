def success_response(data=None, status_code=200):
    response = {
        "status": "success",
        "data": data
    }
    return response, status_code


def error_response(message, status_code=400, errors=None):
    response = {
        "status": "error",
        "message": message
    }
    if errors:
        response["errors"] = errors

    return response, status_code
