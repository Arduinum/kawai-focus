import json

from kawai_focus.main import Logger


class ReadJson:
    """Класс для чтения json файла"""

    def __init__(self, file_name: str):
        self.file_name = file_name
        self.json_data = self.read_json_as_dict()

    def read_json_as_dict(self) -> dict:
        """Метод для чтения json файла как dict"""

        try:
            file_path = f'json/{self.file_name}'
            with open(file=file_path, mode='r') as file:
                return json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError) as err:
            Logger.error(f'Logger: {err.__class__.__name__}: {err}')

    def get_text(self, name: str) -> str:
        """Метод для возврата текста из файла json по ключу name"""
        
        text = self.json_data.get(name)
        
        if text:
            if isinstance(text, list):
                text = ''.join(text)
                return text
            return text


read_json_err = ReadJson(file_name='errors.json')
read_json_timer = ReadJson(file_name='timer.json')
