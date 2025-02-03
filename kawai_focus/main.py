import kivy
kivy.require('2.3.1')

from kivy.app import App


class KawaiFocusApp(App):
    """Класс для создания приложения"""
    
    title = 'Kawai.Focus'
    
    def build(self):
        pass


def main() -> None:
    """Главная функция для запуска приложения KawaiFocus"""

    try:
        KawaiFocusApp().run()
    except KeyboardInterrupt:
        pass
