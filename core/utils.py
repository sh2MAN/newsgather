from loguru import logger
from starlette.requests import Request

logger.add(
    'logging.log', format="{name} {message}", level="INFO", rotation="5MB"
)


def get_db(request: Request):
    """Возвращает текущую сессию."""
    return request.state.db
