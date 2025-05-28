import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic import command

from kawai_focus.schemas import TimerModel
from kawai_focus.database.session import db
from kawai_focus.database.models import Timer, Base
from kawai_focus.database.cruds import list_timers, get_timer, new_timer, update_timer, del_timer


@pytest.fixture(scope='function')
def test_db() -> sessionmaker:
    """Создание тестовой базы данных и сессии"""

    engine = create_engine('sqlite:///:memory:')  # Временная БД
    Base.metadata.create_all(engine)
    alembic_cfg = Config('./alembic.ini')    
    alembic_cfg.set_main_option('script_location', './kawai_focus/database/alembic')
    command.upgrade(alembic_cfg, 'head')
    
    session = sessionmaker(bind=engine)
    db._session_factory = session
    
    return db._session_factory


def test_new_timer(test_db: sessionmaker):
    """Тест crud создания нового таймера"""

    timer_data = TimerModel(title='test_timer_1', pomodoro_time=60, break_long_time=30, break_time=6,count_pomodoro=5)

    with test_db() as session:
        timer = new_timer(data=timer_data)
    
    assert timer.title == 'test_timer_1'
    assert timer.pomodoro_time == 60
    assert timer.break_long_time == 30
    assert timer.break_time == 6
    assert timer.count_pomodoro ==5


def test_get_timer(test_db: sessionmaker):
    """Тест crud получения таймера по id"""

    timer_data = TimerModel(title='test_timer_1', pomodoro_time=60, break_long_time=30, break_time=6,count_pomodoro=5)

    with test_db() as session:
        new_timer(data=timer_data)
        timer = get_timer(timer_id=1)

    assert timer
    assert timer.title == 'test_timer_1'
    assert timer.pomodoro_time == 60
    assert timer.break_long_time == 30
    assert timer.break_time == 6
    assert timer.count_pomodoro ==5


def test_update_timer(test_db: sessionmaker):
    """Тест crud обновления таймера"""

    timer_data = TimerModel(title='test_timer_1', pomodoro_time=60, break_long_time=30, break_time=6,count_pomodoro=5)

    with test_db() as session:
        new_timer(data=timer_data)
        new_timer_data = TimerModel(
            id=1, 
            title='test_timer_2', 
            pomodoro_time=55, 
            break_long_time=25, 
            break_time=5, 
            count_pomodoro=6
        )
        
        timer = update_timer(data=new_timer_data)
    
    assert timer
    assert timer.title == 'test_timer_2'
    assert timer.pomodoro_time == 55
    assert timer.break_long_time == 25
    assert timer.break_time == 5
    assert timer.count_pomodoro == 6


def test_del_timer(test_db: sessionmaker):
    """Тест crud удаления таймера"""

    timer_data = TimerModel(title='test_timer_1', pomodoro_time=60, break_long_time=30, break_time=6,count_pomodoro=5)

    with test_db() as session:
        new_timer(data=timer_data)

        del_timer(timer_id=1)
        timer = session.query(Timer).filter_by(title='test_timer_1').first()

    assert timer is None


def test_list_timers(test_db: sessionmaker):
    """Тест crud получения списка таймеров"""

    timer_data_1 = TimerModel(
        title='test_timer_1', 
        pomodoro_time=60, 
        break_long_time=30, 
        break_time=6, 
        count_pomodoro=5
    )
    timer_data_2 = TimerModel(
        title='test_timer_2', 
        pomodoro_time=55, 
        break_long_time=25, 
        break_time=5, 
        count_pomodoro=6
    )

    with test_db() as session:
        new_timer(data=timer_data_1)
        new_timer(data=timer_data_2)

        timers = list_timers()

    assert timers
    assert timers[0].id == 1
    assert timers[0].title == 'test_timer_1'
    assert timers[1].id == 2
    assert timers[1].title == 'test_timer_2'
