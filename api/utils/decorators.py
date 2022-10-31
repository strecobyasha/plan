from functools import wraps

from flask import jsonify, request


def json_response(f):
    """ Converting response model into json. """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        result_dict = f(*args, **kwargs)
        return jsonify(**result_dict.dict(by_alias=True))

    return decorated_function


def unpack_models(f):
    """ Converting entrance models into kwargs params of the function. """

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if (body := request.context.body) is not None:
            kwargs.update({'body': body})

        if (query := request.context.query) is not None:
            kwargs.update({'query': query})

        if (headers := request.context.headers) is not None:
            kwargs.update({'headers': headers})

        return f(*args, **kwargs)

    return decorated_function
