def validate_title(title):
    if title is None:
        return {"Error": "title is required"}
    elif not isinstance(title, str):
        return {"Error": "title must be of type string"}
    elif len(title) == 0:
        return {"Error": "title can't be an empty string"}
    return None
