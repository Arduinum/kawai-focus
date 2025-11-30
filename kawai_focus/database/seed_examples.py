from sqlalchemy import insert

from kawai_focus.schemas import TimerModel
from kawai_focus.database.session import db
from kawai_focus.database.models import Timer


examples_data = [
    TimerModel(
        title='Timer mini example',
        pomodoro_time=10,
        break_time=3,
        break_long_time=15,
        count_pomodoro=2
    ),
    TimerModel(
        title='Timer max example',
        pomodoro_time=90,
        break_time=10,
        break_long_time=40,
        count_pomodoro=8
    )
]


def new_timer(data: TimerModel) -> TimerModel:
    """Функция для создания нового таймера"""

    with db.get_session() as session:
        query = insert(Timer).values(**data.model_dump()).returning(Timer)
        result = session.execute(query)
        
        new_timer = result.scalar_one()
        session.commit()

        return TimerModel.model_validate(obj=new_timer, from_attributes=True)


def filling_example_temers(data: list[TimerModel]) -> None:
    """Заполняет базу данных образцами таймеров"""

    for timer_model in data:
        with db.get_session() as session:
            query = insert(Timer).values(**timer_model.model_dump()).returning(Timer)
            session.execute(query)
            session.commit()


def main_filling_data():
    """Главная функция заполнения данных бд"""

    filling_example_temers(data=examples_data)
