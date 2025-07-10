from kivy.uix.textinput import TextInput


class BaseNumBehavior:
    """Псевдо-интерфейс для числового ввода"""

    def increment(self):
        raise NotImplementedError('Метод increment() должен быть реализован')

    def decrement(self):
        raise NotImplementedError('Метод decrement() должен быть реализован')


class TimeTomatoInput(TextInput, BaseNumBehavior):
    """Класс для поля ввода колличества помидорово"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '25'
        self.halign = 'center'

    def increment(self):
        """Метод для прибавки 1"""

        if int(self.text) < 90:
            self.text = str(int(self.text) + 1)
    
    def decrement(self):
        """Метод для вычитания 1"""
        
        if int(self.text) > 10:
            self.text = str(int(self.text) - 1)


class TimeBreakInput(TextInput, BaseNumBehavior):
    """Класс для поля ввода времени перерыва"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '5'
        self.halign = 'center'

    def increment(self):
        """Метод для прибавки 1"""

        if int(self.text) < 10:
            self.text = str(int(self.text) + 1)
    
    def decrement(self):
        """Метод для вычитания 1"""
        
        if int(self.text) > 3:
            self.text = str(int(self.text) - 1)


class TimeLoongBreakInput(TextInput, BaseNumBehavior):
    """Класс для поля ввода времени длительного перерыва"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '15'
        self.halign = 'center'

    def increment(self):
        """Метод для прибавки 1"""

        if int(self.text) < 40:
            self.text = str(int(self.text) + 1)
    
    def decrement(self):
        """Метод для вычитания 1"""
        
        if int(self.text) > 15:
            self.text = str(int(self.text) - 1)


class CountTomatosInput(TextInput, BaseNumBehavior):
    """Класс для поля ввода количества помидоров"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = '4'
        self.halign = 'center'

    def increment(self):
        """Метод для прибавки 1"""

        if int(self.text) < 8:
            self.text = str(int(self.text) + 1)
    
    def decrement(self):
        """Метод для вычитания 1"""
        
        if int(self.text) > 2:
            self.text = str(int(self.text) - 1)
