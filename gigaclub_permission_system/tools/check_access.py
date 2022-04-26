from functools import wraps


def check_access(f, access_right):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        return f(self, *args, **kwargs)

    return wrapper
