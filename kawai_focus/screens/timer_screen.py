from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from kawai_focus.utils.utils import data_json, custom_timer, calculate_time


class TimerScreen(Screen):
    """Экран таймера"""

    sound_timer_name = data_json.get_text('sound_timer')
    path_file = f'sounds/{sound_timer_name}'
    sound = SoundLoader.load(path_file)

    def __init__(self, **kwargs):
        super(TimerScreen, self).__init__(**kwargs)
        # Переменные для управления таймером
        self.zero_time = data_json.get_text('zero_time')
        self.timer_generator = None 
        self.paused = False
        self.remaining_time = None
        self.sound_stop_event = None
        self.timer = None
        self.timer_start_time = None
        self.source_timer_names = None

    def choice_timer(self) -> None:
        """Метод для выбора таймера"""
        
        current_timer_name = self.manager.state_machine.pop(0)
        
        if current_timer_name == 'pomodoro':
            self.timer_generator = custom_timer(mm_user=self.timer.pomodoro_time)
            self.ids.time_label.text = calculate_time(mm_user=self.timer.pomodoro_time)
            self.ids.type_timer_label.text = 'Помидор'
        elif current_timer_name == 'break':
            self.timer_generator = custom_timer(mm_user=self.timer.break_time)
            self.ids.time_label.text = calculate_time(mm_user=self.timer.break_time)
            self.ids.type_timer_label.text = 'Перерыв'
        else:
            self.timer_generator = custom_timer(mm_user=self.timer.break_long_time)
            self.ids.time_label.text = calculate_time(mm_user=self.timer.break_long_time)
            self.ids.type_timer_label.text = 'Перерывище'

        self.ids.stop_button.opacity = 0
        self.ids.stop_button.disabled = True

    def start_timer(self, instance) -> None:
        """Метод для запуска таймера"""
        
        if self.paused:
            self.paused = False
        else:
            # Инициализация генератора таймера
            if len(self.manager.state_machine) and self.timer_generator is None:
                self.choice_timer()
            
            self.ids.stop_button.opacity = 1
            self.ids.stop_button.disabled = False
            
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
        self.remaining_time = next(self.timer_generator, self.zero_time)
        self.ids.time_label.text = self.timer_start_time
        self.sound.stop()

        if self.sound_stop_event:
            Clock.unschedule(self.sound_stop_event)
            self.sound_stop_event = None

        if not len(self.manager.state_machine):
            self.manager.state_machine = self.source_timer_names.copy()

        self.choice_timer()    

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
