import uuid


def get_new_id() -> str:
    return str(uuid.uuid4())
