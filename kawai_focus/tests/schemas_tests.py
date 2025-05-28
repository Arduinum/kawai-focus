import pytest
from pydantic import ValidationError

from kawai_focus.utils.errors import ErrorMessage
from kawai_focus.schemas import TimerTimeModel


def test_valid_time():
    """Тест корректных данных"""
    
    timer = TimerTimeModel(hh=10, mm=30, ss=15)
    assert timer.hh == 10
    assert timer.mm == 30
    assert timer.ss == 15


def test_not_int_type():
    """Тест исключения для некорректного типа данных"""
    
    with pytest.raises(ValidationError) as excinfo:
        TimerTimeModel(hh=None, mm=30, ss=15)

    assert 'Input should be a valid integer' in str(excinfo.value)


def test_no_time():
    """Тест исключения ситуации когда не указано время"""
    
    with pytest.raises(ValueError) as excinfo:
        TimerTimeModel(hh=0, mm=0, ss=0)

    assert ErrorMessage.NO_TIME.value in str(excinfo.value)


def test_negative_time():
    """Тест исключения для отрицательного времени"""
    
    with pytest.raises(ValueError) as excinfo:
        TimerTimeModel(hh=-1, mm=30, ss=15)

    assert 'Input should be greater than or equal to 0' in str(excinfo.value)


def test_exceed_seconds_or_minutes():
    """Тест исключения для секунд/минут больше 59"""
    
    with pytest.raises(ValueError) as excinfo:
        TimerTimeModel(hh=0, mm=60, ss=10)

    assert 'Input should be less than or equal to 59' in str(excinfo.value)


def test_exceed_hours():
    """Тест исключения для часов больше 23"""
    
    with pytest.raises(ValueError) as excinfo:
        TimerTimeModel(hh=24, mm=0, ss=0)

    assert 'Input should be less than or equal to 23' in str(excinfo.value)
