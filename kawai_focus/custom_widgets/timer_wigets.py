from kivy.uix.textinput import TextInput



class BaseNumInput(TextInput):
    """Базовый класс для поля числа"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '0'
        self.halign = 'center'

    def increment(self):
        """Метод для прибавки 1"""

        self.text = str(int(self.text) + 1)

    def decrement(self):
        """Метод для вычитания 1"""
        
        self.text = str(int(self.text) - 1)


class TimeTomatoInput(BaseNumInput):
    """Класс для поля ввода колличества помидорово"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '25'


class TimeBreakInput(BaseNumInput):
    """Класс для поля ввода времени перерыва"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '5'

class TimeLoongBreakInput(BaseNumInput):
    """Класс для поля ввода времени длительного перерыва"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '15'


class CountTomatosInput(BaseNumInput):
    """Класс для поля ввода количества помидоров"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '4'
