from kivy.uix.screenmanager import Screen

from kawai_focus.utils.utils import calculate_time, gen_types_timers
from kawai_focus.database.cruds import get_timer


class TimersScreen(Screen):
    """Экран таймеры"""

    def __init__(self, **kwargs):
        super(TimersScreen, self).__init__(**kwargs)
    
    
    def switch_new_timer(self, instance) -> None:
        """Метод для переключения на экран Конструктор таймера"""

        self.manager.current = 'timer_constructor_screen'


    def switch_timer(self, instance) -> None:
        """Метод для кнопки переключения на выбранный таймер"""

        timer = get_timer(timer_id=instance.timer_id)
        screen_timer = self.manager.get_screen('timer_screen')
        screen_timer.timer = timer
        time_culc = calculate_time(mm_user=timer.pomodoro_time)
        screen_timer.timer_start_time = time_culc
        screen_timer.ids.time_label.text = time_culc
        screen_timer.ids.title_label.text = timer.title
        screen_timer.source_timer_names = gen_types_timers(count_pomodoro=timer.count_pomodoro)

        self.manager.state_machine = screen_timer.source_timer_names.copy()
        self.manager.current = 'timer_screen'
