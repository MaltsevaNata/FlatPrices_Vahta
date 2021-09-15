from pydantic import ValidationError


def validate(cls, err_callback):
    def outer(func):
        def inner(socket, data, **kwargs):
            try:
                m = cls(**data)
                return func(socket, m, **kwargs)
            except ValidationError as e:
                err_callback(socket, e.json())
        return inner
    return outer