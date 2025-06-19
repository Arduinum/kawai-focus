import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.logger import Logger

import logging

from kawai_focus.screens.timer_screen import TimerScreen
from kawai_focus.screens.timer_constructor_screen import TimerConstructorScreen


Logger.setLevel(logging.DEBUG)


class KawaiFocusApp(App):
    """Класс для создания приложения"""

    title = 'Kawai.Focus'

    def build(self):
        # Загрузка kv файла
        Builder.load_file('kv/timer_screen.kv')
        Builder.load_file('kv/timer_constructor_screen.kv')

        screen_manager = ScreenManager()
        screen_manager.add_widget(TimerConstructorScreen(name='timer_constructor_screen'))
        screen_manager.add_widget(TimerScreen(name='timers_screen'))
        return screen_manager


def main() -> None:
    """Главная функция для запуска приложения KawaiFocus"""

    try:
        KawaiFocusApp().run()
    except KeyboardInterrupt:
        pass
