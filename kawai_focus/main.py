import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.logger import Logger

import logging

from kawai_focus.screens.timer_screen import TimerScreen
from kawai_focus.screens.timer_constructor_screen import TimerConstructorScreen
from kawai_focus.screens.timers_screen import TimersScreen
from kawai_focus.database.cruds import list_timers


Logger.setLevel(logging.DEBUG)


class KawaiFocusApp(App):
    """Класс для создания приложения"""

    title = 'Kawai.Focus'

    def build(self):
        # Загрузка kv файла
        Builder.load_file('kv/timer_screen.kv')
        Builder.load_file('kv/timer_constructor_screen.kv')
        Builder.load_file('kv/timers_screen.kv')

        screen_manager = ScreenManager()
        timers = list_timers()
        timers_screen = TimersScreen(name='timers_screen')
        timers_screen.ids.timers_view.data = timers
        
        screen_manager.add_widget(timers_screen)
        screen_manager.add_widget(TimerConstructorScreen(name='timer_constructor_screen'))
        screen_manager.add_widget(TimerScreen(name='timer_screen'))
        return screen_manager


def main() -> None:
    """Главная функция для запуска приложения KawaiFocus"""

    try:
        KawaiFocusApp().run()
    except KeyboardInterrupt:
        pass
