from typing import Generator
import json
from os import path, listdir

from kawai_focus.main import Logger
from kawai_focus.utils.errors import ErrorMessage
from kawai_focus.utils.validators import TimerValidator


class ReadJson:
    """Класс для чтения всех JSON-файлов в директории и объединения их в словарь."""

    def __init__(self, folder_json: str):
        self.folder_json = folder_json
        self._json_data = self._read_all_json()

    def _read_all_json(self) -> dict:
        """Читает все JSON-файлы в директории и возвращает объединённый словарь."""
        
        if not path.exists(self.folder_json):
            raise FileNotFoundError(ErrorMessage.FOLDER_NOT_FOUND.value)

        # Получаем список всех файлов с расширением .json
        json_files = [path.join(self.folder_json, file) for file in listdir(self.folder_json) if file.endswith('.json')]

        if not json_files:
            raise FileNotFoundError(ErrorMessage.JSON_NOT_FOUND.value)

        data_dict = {}
        
        for file_path in json_files:
            with open(file_path, 'r', encoding='utf-8') as file:
                # Обновляем словарь с помощью .update() для эффективности
                data_dict.update(json.load(file))

        return data_dict

    def get_text(self, name: str) -> str:
        """Возвращает текст из словаря по ключу."""
        
        return self._json_data.get(name, ErrorMessage.KEY_ERROR.value)


data_json = ReadJson(folder_json='json')


def custom_timer(valid_data: TimerValidator) -> Generator[str, None, None]:
    """Функция отсчитывает время, установленное для таймера в формате 
    'hh:mm:ss'. Возвращает генератор, который возвращает текущее время
    в формате 'hh:mm:ss'."""

    try:
        total_seconds = (int(valid_data.hh) * 3600) + (int(valid_data.mm) * 60) + (int(valid_data.ss))

        for remaining in range(total_seconds, -1, -1):
            yield f"{remaining // 3600:02d}:{(remaining % 3600) // 60:02d}:{remaining % 60:02d}"
    except (TypeError, ValueError) as err:
        Logger.error(f'Logger: {err.__class__.__name__}: {err}')
    