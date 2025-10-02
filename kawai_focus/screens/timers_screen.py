from kivy.properties import StringProperty, NumericProperty
from kivymd.uix.screen import MDScreen
from kivymd.uix.expansionpanel import MDExpansionPanel

from kawai_focus.utils.utils import calculate_time, gen_types_timers
from kawai_focus.database.cruds import get_timer, list_timers
from kawai_focus.main import Logger


class ExpansionPanelItem(MDExpansionPanel):
    """Кастомный элемент панели с данными таймера"""

    timer_id = NumericProperty()
    title = StringProperty()
    info = StringProperty()


class TimersScreen(MDScreen):
    """Экран таймеры"""

    def on_enter(self, *args) -> None:
        """Загружает список таймеров при входе на экран"""
        
        self.load_timers()

    def load_timers(self) -> None:
        """Загружает все таймеры и добавляет их в контейнер"""

        self.ids.container.clear_widgets()
        all_timers = list_timers()

        for timer_data in all_timers:
            panel = ExpansionPanelItem(
                timer_id=timer_data.get('timer_id'), 
                title=timer_data.get('title'),
                info=timer_data.get('info'),
            )
            self.ids.container.add_widget(panel)

    def switch_timer(self, instance) -> None:
        """Метод для кнопки переключения на выбранный таймер"""
        
        timer = get_timer(timer_id=instance.timer_id)
        if not timer:
            Logger.warning(f'Таймер с ID {instance.timer_id} не найден!')
            return

        screen_timer = self.manager.get_screen('timer_screen')
        screen_timer.timer = timer
        time_calc = calculate_time(mm_user=timer.pomodoro_time)
        screen_timer.timer_start_time = time_calc
        screen_timer.ids.time_label.text = time_calc
        screen_timer.ids.title_label.text = timer.title
        screen_timer.source_timer_names = gen_types_timers(count_pomodoro=timer.count_pomodoro)

        self.manager.state_machine = screen_timer.source_timer_names.copy()
        self.manager.current = 'timer_screen'
