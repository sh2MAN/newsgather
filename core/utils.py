from starlette.requests import Request


def get_db(request: Request):
    """Возвращает текущую сессию."""
    return request.state.db
