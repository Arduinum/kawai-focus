from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from os.path import isfile

from kawai_focus.utils.utils import data_json, custom_timer, calculate_time
from kawai_focus.main import Logger


class TimerScreen(MDScreen):
    """Экран таймера"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.load_sound)

        # Переменные для управления таймером
        self.zero_time = data_json.get_text('zero_time')
        self.timer_generator = None
        self.paused = False
        self.remaining_time = None
        self.sound_stop_event = None
        self.timer = None
        self.timer_start_time = None
        self.source_timer_names = None
        self.sound = None  # Заглушка

    def load_sound(self, dt) -> None:
        sound_timer_name = data_json.get_text('sound_timer')
        path_file = f'sounds/{sound_timer_name}'
        
        if not isfile(path_file):
            Logger.error(f'[TimerScreen] Файл звука не найден: {path_file}')
            return
        
        self.sound = SoundLoader.load(path_file)
        
        if not self.sound:
            Logger.error(f'[TimerScreen] Не удалось загрузить файл звука (неподдерживаемый формат?): {path_file}')
            return

    def on_pre_enter(self, *args) -> None:
        """Вызывается перед появлением экрана"""
        
        # Прячем кнопки "Стоп" и "Пауза"
        self.ids.stop_button.opacity = 0
        self.ids.stop_button.disabled = True

        self.ids.pause_button.opacity = 0
        self.ids.pause_button.disabled = True

        # Проверяем состояние state_machine
        if not hasattr(self.manager, 'state_machine') or self.manager.state_machine is None:
            self.manager.state_machine = []

    def choice_timer(self) -> None:
        """Выбор таймера (помидор / перерыв / длинный перерыв)"""
        
        if not self.manager.state_machine:
            return

        current_timer_name = self.manager.state_machine.pop(0)

        match current_timer_name:
            case 'pomodoro':
                self.timer_generator = custom_timer(mm_user=self.timer.pomodoro_time)
                self.ids.time_label.text = calculate_time(self.timer.pomodoro_time)
                self.ids.type_timer_label.text = 'Помидор'
            case 'break':
                self.timer_generator = custom_timer(mm_user=self.timer.break_time)
                self.ids.time_label.text = calculate_time(self.timer.break_time)
                self.ids.type_timer_label.text = 'Перерыв'
            case _:
                self.timer_generator = custom_timer(mm_user=self.timer.break_long_time)
                self.ids.time_label.text = calculate_time(self.timer.break_long_time)
                self.ids.type_timer_label.text = 'Перерывище'

    def start_timer(self, *args) -> None:
        """Запуск таймера"""
        
        # Делаем кнопки панели навишгации неактивными
        self.ids.nav_panel.ids.menu.disabled = True
        self.ids.nav_panel.ids.timers_nav.disabled = True
        self.ids.nav_panel.ids.guide_nav.disabled = True
        self.ids.nav_panel.ids.info_nav.disabled = True

        # Активируем кнопки "Стоп" и "Пауза"
        self.ids.stop_button.opacity = 1
        self.ids.stop_button.disabled = False

        self.ids.pause_button.opacity = 1
        self.ids.pause_button.disabled = False

        # Прячем кнопку "Старт"
        self.ids.start_button.opacity = 0
        self.ids.start_button.disabled = True

        if self.paused:
            self.paused = False
        else:
            if len(self.manager.state_machine) and self.timer_generator is None:
                self.choice_timer()

            self.remaining_time = next(self.timer_generator, self.zero_time)

        Clock.schedule_interval(self.update_time, 1)

    def pause_timer(self, *args) -> None:
        """Пауза таймера"""
        
        if not self.paused:
            self.paused = True
            Clock.unschedule(self.update_time)
        
        # Активируем кнопку "Старт"
        self.ids.start_button.opacity = 1
        self.ids.start_button.disabled = False

        # Прячем кнопку "Пауза"
        self.ids.pause_button.opacity = 0
        self.ids.pause_button.disabled = True

    def stop_timer(self, *args) -> None:
        """Остановка таймера"""
        
        Clock.unschedule(self.update_time)
        self.paused = False

        # Сбрасываем оставшееся время
        self.remaining_time = next(self.timer_generator, self.zero_time)
        self.ids.time_label.text = self.timer_start_time

        # Останавливаем звук, если играет
        if self.sound:
            self.sound.stop()

        if self.sound_stop_event:
            Clock.unschedule(self.sound_stop_event)
            self.sound_stop_event = None

        # Возврат цикла таймеров
        if not len(self.manager.state_machine):
            self.manager.state_machine = self.source_timer_names.copy()

        # Делаем кнопки панели навишгации неактивными
        self.ids.nav_panel.ids.menu.disabled = False
        self.ids.nav_panel.ids.timers_nav.disabled = False
        self.ids.nav_panel.ids.guide_nav.disabled = False
        self.ids.nav_panel.ids.info_nav.disabled = False

        # Прячем кнопки "Стоп" и "Пауза"
        self.ids.stop_button.opacity = 0
        self.ids.stop_button.disabled = True

        self.ids.pause_button.opacity = 0
        self.ids.pause_button.disabled = True

        # Активируем кнопку "Старт"
        self.ids.start_button.opacity = 1
        self.ids.start_button.disabled = False

        self.choice_timer()

    def play_sound(self, *args) -> None:
        """Воспроизведение звука"""

        if self.sound:
            self.sound.play()
            self.sound_stop_event = Clock.schedule_once(lambda dt: self.sound.stop(), 20)

    def update_time(self, dt) -> None:
        """Обновление времени"""
        
        if self.paused:
            return

        self.remaining_time = next(self.timer_generator, self.zero_time)
        self.ids.time_label.text = self.remaining_time

        if self.remaining_time == self.zero_time:
            Clock.unschedule(self.update_time)
            Clock.schedule_once(self.play_sound)
