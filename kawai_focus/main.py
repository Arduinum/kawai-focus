import kivy
kivy.require('2.3.1')

from kivy.lang import Builder
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivy.logger import Logger
from kivy.properties import StringProperty
from kivy import Config

import logging

from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.behaviors import RotateBehavior 
from kivymd.uix.list import MDListItemTrailingIcon
from kivymd.uix.navigationrail import MDNavigationRailItem
from kivymd.uix.boxlayout import MDBoxLayout

from kawai_focus.menu_app import MenuApp
from kawai_focus.screens.timers_screen import TimersScreen
from kawai_focus.screens.timer_screen import TimerScreen


Logger.setLevel(logging.DEBUG)

Config.set('kivy', 'audio', 'ffpyplayer')  # вместо audio_sdl2


class TrailingPressedIconButton(
    ButtonBehavior, RotateBehavior, MDListItemTrailingIcon
): 
    """Кнопка-иконка в конце элемента списка с поддержкой анимации"""
    ...


class CommonNavigationRailItem(MDNavigationRailItem):
    """Класс панель навигации"""
    
    text = StringProperty()
    icon = StringProperty()


class KawaiFocusApp(MDApp, MenuApp):
    """Главный класс приложения"""

    title = 'Kawai-Focus'
    icon = 'images/icon.png'

    def build(self) -> MDScreenManager:
        """Создаёт и возвращает менеджер экранов приложения"""
        
        self.theme_cls.theme_style = 'Dark'
        # Загрузка kv файла
        Builder.load_file('kv/timers_screen.kv')
        Builder.load_file('kv/timer_screen.kv')

        self.screen_manager = MDScreenManager()
        self.screen_manager.add_widget(TimersScreen(name='timers_screen'))
        self.screen_manager.add_widget(TimerScreen(name='timer_screen'))

        return self.screen_manager

    def tap_expansion_chevron(
        self, panel: MDExpansionPanel, chevron: TrailingPressedIconButton
    ) -> None:
        """Анимация и переключение состояния раскрытия панели"""
        
        Animation(
            padding=(
                [0, dp(12), 0, dp(12)] if not panel.is_open else [0, 0, 0, 0]
            ),
            d=0.2,
        ).start(panel)
        panel.open() if not panel.is_open else panel.close()
        (
            panel.set_chevron_down(chevron)
            if not panel.is_open
            else panel.set_chevron_up(chevron)
        )


def main() -> None:
    """Главная функция для запуска приложения KawaiFocus"""

    try:
        KawaiFocusApp().run()
    except KeyboardInterrupt:
        pass
