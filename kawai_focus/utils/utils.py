from typing import Generator

from kawai_focus.main import Logger
from kawai_focus.utils.data_json import read_json_err


def custom_timer(hh: int=0, mm: int=0, ss: int=0) -> Generator[str, None, None]:
    """Функция отсчитывает время, установленное для таймера в формате 
    'hh:mm:ss'. Возвращает генератор, который возвращает текущее время
    в формате 'hh:mm:ss'."""

    try:
        if ss == 0 and mm == 0 and hh == 0:
            raise ValueError(read_json_err.get_text('no_time'))
        
        if ss < 0 or mm < 0 or hh < 0:
            raise ValueError(read_json_err.get_text('negative_time'))

        if ss > 59 or mm > 59:
            raise ValueError(read_json_err.get_text('ss_mm_big'))
        
        if hh > 23:
            raise ValueError(read_json_err.get_text('hh_big'))

        total_seconds = (int(hh or 0) * 3600) + (int(mm or 0) * 60) + (int(ss or 0))

        for remaining in range(total_seconds, -1, -1):
            yield f"{remaining // 3600:02d}:{(remaining % 3600) // 60:02d}:{remaining % 60:02d}"
    except (TypeError, ValueError) as err:
        Logger.error(f'Logger: {err.__class__.__name__}: {err}')
