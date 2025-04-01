from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.core.audio import SoundLoader


from kawai_focus.utils.utils import custom_timer
from kawai_focus.utils.data_json import read_json_timer


class TimerScreen(Screen):
    """Экран таймера"""

    sound_timer_name = read_json_timer.get_text('sound_timer')
    path_file = f'sounds/{sound_timer_name}'
    sound = SoundLoader.load(path_file)

    def __init__(self, **kwargs):
        super(TimerScreen, self).__init__(**kwargs)
        # Переменные для управления таймером
        self.zero_time = read_json_timer.get_text('zero_time')
        self.timer_generator = None
        self.paused = False
        self.remaining_time = None
        self.sound_stop_event = None

    def start_timer(self, instance) -> None:
        """Метод для запуска таймера"""
        
        if self.paused:
            self.paused = False
        else:
            # Инициализация генератора таймера
            self.timer_generator = custom_timer(ss=12)  # Установите необходимое время
            self.remaining_time = next(self.timer_generator, self.zero_time)
        
        # Запуск обновления времени каждую секунду
        Clock.schedule_interval(self.update_time, 1)

    def pause_timer(self, instance) -> None:
        """Метод для паузы таймера"""
        
        if not self.paused:
            self.paused = True
            # Остановка обновления времени
            Clock.unschedule(self.update_time)

    def stop_timer(self, instance) -> None:
        """Метод для остановки таймера"""
        
        # Остановка обновления времени
        Clock.unschedule(self.update_time)
        self.paused = False
        # TODO: временное решение, время будет задаваться в интерфейсе
        self.remaining_time = read_json_timer.get_text('custom_time')
        self.ids.time_label.text = self.remaining_time

        self.sound.stop()

        if self.sound_stop_event:
            Clock.unschedule(self.sound_stop_event)
            self.sound_stop_event = None

    def play_sound(self, dt) -> None:
        """Метод для воспроизведения звука"""

        self.sound.play()
        # Планируем остановку звука через 20 секунд
        self.sound_stop_event = Clock.schedule_once(lambda dt: self.sound.stop(), 20)

    def update_time(self, dt) -> None:
        """Метод для обновления времени на экране"""

        if self.paused:
            return

        # Получение следующего значения времени из генератора
        self.remaining_time = next(self.timer_generator, self.zero_time)
        self.ids.time_label.text = self.remaining_time
        
        if self.remaining_time == self.zero_time:
            # Остановка обновления времени
            Clock.unschedule(self.update_time)
            Clock.schedule_once(self.play_sound)
