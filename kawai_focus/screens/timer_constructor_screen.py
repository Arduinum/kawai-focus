from kivy.uix.screenmanager import Screen

from kawai_focus.custom_widgets.timer_wigets import TimeTomatoInput
from kawai_focus.schemas import TimerModel
from kawai_focus.database.cruds import new_timer
from kawai_focus.utils.utils import calculate_time, gen_types_timers
from kawai_focus.screens.validators_fields import validate_title


class TimerConstructorScreen(Screen):
    """Экран конструктора таймера"""

    def __init__(self, **kwargs):
        super(TimerConstructorScreen, self).__init__(**kwargs)
    
    def create_timer(self, instance):
        """Метод для создания таймера"""

        validate_title(self, self.ids.title.text)

        # прекратить создание таймера если поле пустое
        if not self.ids.title.text:
            return  

        timer = new_timer(
            data=TimerModel(
                title=self.ids.title.text,
                pomodoro_time=int(self.ids.time_tomato_input.text),
                break_time=int(self.ids.time_break_input.text),
                break_long_time=int(self.ids.time_long_break_input.text),
                count_pomodoro=int(self.ids.count_tomatos_input.text)
            )
        )

        if timer:
            screen_timer = self.manager.get_screen('timers_screen')
            screen_timer.timer = timer
            time_culc = calculate_time(mm_user=timer.pomodoro_time)
            screen_timer.timer_start_time = time_culc
            screen_timer.ids.time_label.text = time_culc
            screen_timer.source_timer_names = gen_types_timers(count_pomodoro=timer.count_pomodoro)

            self.manager.state_machine = screen_timer.source_timer_names.copy()
            self.manager.current = 'timers_screen'


    def back(self, instance) -> None:
        """Метод для кнопки назад - возврат в меню таймеров"""

        pass
