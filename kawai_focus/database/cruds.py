from sqlalchemy import select, insert, update, delete

from kawai_focus.schemas import TimerModel, TimerListModel
from kawai_focus.database.session import db
from kawai_focus.database.models import Timer
from kawai_focus.database.decor_erors import crud_error_guard


@crud_error_guard
def get_timer(timer_id: int) -> TimerModel:
    """Функция для получения данных таймера"""

    with db.get_session() as session:
        query = select(
            Timer.id, 
            Timer.title,
            Timer.pomodoro_time, 
            Timer.break_time, 
            Timer.break_long_time,
            Timer.count_pomodoro
        ).where(timer_id == Timer.id)
        result = session.execute(query)
        timer = result.mappings().first()

        return TimerModel.model_validate(obj=timer, from_attributes=True)


@crud_error_guard
def list_timers() -> list[TimerListModel]:
    """Функция для получения списка таймеров"""

    with db.get_session() as session:
        query = select(Timer.id, Timer.title)
        result = session.execute(query)
        timers = result.mappings().fetchall()
        
        return [TimerListModel.model_validate(obj=accept, from_attributes=True) for accept in timers]


@crud_error_guard
def new_timer(data: TimerModel) -> TimerModel:
    """Функция для создания нового таймера"""

    with db.get_session() as session:
        query = insert(Timer).values(**data.model_dump()).returning(Timer)
        result = session.execute(query)
        
        new_timer = result.scalar_one()
        session.commit()

        return TimerModel.model_validate(obj=new_timer, from_attributes=True)


@crud_error_guard
def update_timer(data: TimerModel) -> TimerModel:
    """Функция для обновления таймера"""

    with db.get_session() as session:
        query = update(Timer).values(**data.model_dump()).where(data.id == Timer.id).returning(Timer)
        result = session.execute(query)
        
        updated_timer = result.scalar_one()
        session.commit()

        return TimerModel.model_validate(obj=updated_timer, from_attributes=True)


@crud_error_guard
def del_timer(timer_id: int) -> None:
    """Функция для удаления таймера"""

    with db.get_session() as session:
        query = delete(Timer).where(timer_id == Timer.id)
        session.execute(query)

        session.commit()
