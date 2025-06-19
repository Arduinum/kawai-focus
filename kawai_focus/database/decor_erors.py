from typing import Any, Callable, Optional
from sqlalchemy.exc import IntegrityError, OperationalError, NoResultFound
from pydantic import ValidationError

from kawai_focus.main import Logger
from kawai_focus.utils.errors import ErrorMessage


def crud_error_guard(func:  Callable[..., Any]) -> Callable[..., Optional[Any]] | None:
    """Декоратор для обработки ошибок CRUD"""

    def wrapper(*args: Any, **kwargs: Any) -> Optional[Any] | None:

        try:
            result = func(*args, **kwargs)
            return result
        except ConnectionError as err:
            Logger.error(f'{ErrorMessage.CONNECTION_ERROR.value}: {err}')
        except IntegrityError as err:
            Logger.error(f'{ErrorMessage.INTEGRITY_ERROR.value}: {err}')
        except OperationalError as err:
            Logger.error(f'{ErrorMessage.OPERATIONAL_ERROR.value}: {err}')
        except ValidationError as err:
            Logger.error(f'{ErrorMessage.VALIDATION_ERROR.value}: {err}')
        except NoResultFound as err:
            Logger.error(f'{ErrorMessage.NO_RESULT_FOUND.value}: {err}')
    return wrapper
