from enum import Enum

class ErrorMessage(Enum):
    NO_TIME = 'Не указано время таймера!'
    NEGATIVE_TIME = 'Время таймера не может быть отрицательным!'
    SS_MM_BIG = 'Секунды и минуты не могут быть больше 59!'
    HH_BIG = 'Часы не могут быть больше 23!'
    FOLDER_NOT_FOUND = 'Папка не найдена!'
    JSON_NOT_FOUND = 'Файл json не найден!'
    TYPE_DICT = 'Тип данных не является словарем!'
    NOT_INT_TYPE = 'Тип данных не является целым числом!'
    KEY_ERROR = 'Ключ не найден!'
