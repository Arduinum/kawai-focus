import time
import re
from typing import Generator
import logging

from kivy.logger import Logger


Logger.setLevel(logging.DEBUG)


def custom_timer(timer_str: str) -> Generator[str, None, None]:
    """Функция отсчитывает время, установленное для таймера в формате 'XhYmZs'."""
    
    try:
        match = re.match(r'(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?', timer_str)
        if not match:
            raise ValueError('Неверный формат времени, используйте "XhYmZs"!')

        hours, minutes, seconds = match.groups()
        total_seconds = (int(hours or 0) * 3600) + (int(minutes or 0) * 60) + (int(seconds or 0))
        
        if total_seconds == 0:
            raise ValueError('Не указано время таймера!')

        for remaining in range(total_seconds, -1, -1):
            yield f"{remaining // 3600:02d}:{(remaining % 3600) // 60:02d}:{remaining % 60:02d}"
    except ValueError as err:
        Logger.error(f'{err.__class__.__name__}: {err}')


if __name__ == '__main__':
    # Пример использования
    
    for time_now in custom_timer('0h1m3s'):
        print(time_now)
