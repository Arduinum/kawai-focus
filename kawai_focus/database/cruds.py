from sqlalchemy import select, insert
from sqlalchemy.exc import SQLAlchemyError, OperationalError, NoResultFound
from pydantic import ValidationError

from kawai_focus.schemas import TimerModel
from kawai_focus.database.session import db
from kawai_focus.database.models import Timer
from kawai_focus.main import Logger


def get_timer(timer_id: int) -> TimerModel:
    """Функция для получения данных таймера"""

    try:
        with db.get_session() as session:
            timer_model = Timer 
            query = select(
                timer_model.id, 
                timer_model.title,
                timer_model.pomodoro_time, 
                timer_model.break_time, 
                timer_model.break_long_time,
                timer_model.count_pomodoro
            ).where(timer_id == timer_model.id)
            result = session.execute(query)
            timer = result.mappings().first()

            return TimerModel.model_validate(obj=timer, from_attributes=True)
    except (ConnectionError, SQLAlchemyError, TimeoutError, OperationalError, ValidationError, NoResultFound) as err:
        Logger.error(f'{err.__class__.__name__}: {err}')


def new_timer(data: TimerModel) -> bool | None:
    """Функция для создания нового таймера"""

    try:
        with db.get_session() as session:
            timer_model = Timer
            query = insert(timer_model).values(**data.model_dump())
            session.execute(query)
            session.commit()
    except (ConnectionError, SQLAlchemyError, TimeoutError, OperationalError, ValidationError) as err:
        Logger.error(f'{err.__class__.__name__}: {err}')
    else:
        return True


if __name__ == '__main__':
    # new_timer(data=TimerValidModel(
    #     title='test_timer_2',
    #     pomodoro_time=50,
    #     break_long_time=25,
    #     break_time=5,
    #     count_pomodoro=4
    # ))

    print(get_timer(timer_id=1))
