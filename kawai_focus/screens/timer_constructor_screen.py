from kivy.uix.screenmanager import Screen

from kawai_focus.custom_widgets.timer_wigets import TimeTomatoInput
from kawai_focus.schemas import TimerModel
from kawai_focus.database.cruds import new_timer


class TimerConstructorScreen(Screen):
    """Экран конструктора таймера"""

    def __init__(self, **kwargs):
        super(TimerConstructorScreen, self).__init__(**kwargs)
    
    def create_timer(self, instance):
        """Метод для создания таймера"""

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
            # Todo: временное решение: нужно сделать механизм для 
            # автоматического рассчёта часов, минут и секунд из 
            # колличества минут, введённого пользователем
            screen_timer.ids.time_label.text = f'00:{
                "0" + str(timer.pomodoro_time) if timer.pomodoro_time <= 9 else timer.pomodoro_time
            }:00'
            self.manager.current = 'timers_screen'


    def back(self, instance) -> None:
        """Метод для кнопки назад - возврат в меню таймеров"""

        pass
