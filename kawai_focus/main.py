import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kawai_focus.screens.timer_screen import TimerScreen


class KawaiFocusApp(App):
    """Класс для создания приложения"""
    
    title = 'Kawai.Focus'
    
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(TimerScreen(name='timers_screen'))
        return screen_manager


def main() -> None:
    """Главная функция для запуска приложения KawaiFocus"""

    try:
        KawaiFocusApp().run()
    except KeyboardInterrupt:
        pass
