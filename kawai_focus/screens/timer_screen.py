from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

from kawai_focus.utils import custom_timer


class TimerScreen(Screen):
    """Экран таймера"""

    def __init__(self, **kwargs):
        super(TimerScreen, self).__init__(**kwargs)

        self.layout = FloatLayout()

        # Добавляем кнопку "Старт"
        self.start_button = Button(
            text='Старт', 
            size_hint=(None, None), 
            height=40, 
            width=100, 
            pos_hint={
                'center_x': 0.3, 
                'center_y': 0.5
            }
        )
        self.start_button.bind(on_release=self.start_timer)
        self.layout.add_widget(self.start_button)

        # Добавляем кнопку "Пауза"
        self.pause_button = Button(
            text='Пауза', 
            size_hint=(None, None), 
            height=40, 
            width=100, 
            pos_hint={
                'center_x': 0.5, 
                'center_y': 0.5
            }
        )
        self.pause_button.bind(on_release=self.pause_timer)
        self.layout.add_widget(self.pause_button)

        # Добавляем кнопку "Стоп"
        self.stop_button = Button(
            text='Стоп', 
            size_hint=(None, None), 
            height=40, 
            width=100, 
            pos_hint={
                'center_x': 0.7, 
                'center_y': 0.5
            }
        )
        self.stop_button.bind(on_release=self.stop_timer)
        self.layout.add_widget(self.stop_button)

        # Добавляем Label для отображения времени
        self.time_label = Label(
            text='00:00:10', 
            size_hint=(None, None), 
            pos_hint={
                'center_x': 0.5, 
                'center_y': 0.6
            }
        )
        self.layout.add_widget(self.time_label)

        self.add_widget(self.layout)

        # Переменные для управления таймером
        self.timer_generator = None
        self.paused = False
        self.remaining_time = None

    def start_timer(self, instance) -> None:
        if self.paused:
            self.paused = False
        else:
            # Инициализация генератора таймера
            self.timer_generator = custom_timer('0h0m10s')  # Установите необходимое время
            self.remaining_time = next(self.timer_generator, '00:00:00')
        
        # Запуск обновления времени каждую секунду
        Clock.schedule_interval(self.update_time, 1)

    def pause_timer(self, instance) -> None:
        if not self.paused:
            self.paused = True
            # Остановка обновления времени
            Clock.unschedule(self.update_time)

    def stop_timer(self, instance) -> None:
        # Остановка обновления времени
        Clock.unschedule(self.update_time)
        self.paused = False
        self.remaining_time = '00:00:00'
        self.time_label.text = self.remaining_time

    def update_time(self, dt) -> None:
        if self.paused:
            return

        try:
            # Получение следующего значения времени из генератора
            self.remaining_time = next(self.timer_generator, '00:00:00')
            self.time_label.text = self.remaining_time

            if self.remaining_time == '00:00:00':
                # Остановка обновления времени
                Clock.unschedule(self.update_time)
        except StopIteration:
            # Остановка обновления времени при завершении генератора
            Clock.unschedule(self.update_time)
