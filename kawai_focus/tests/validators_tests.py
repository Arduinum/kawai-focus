import pytest
from kawai_focus.utils.errors import ErrorMessage
from kawai_focus.utils.validators import TimerValidator


def test_valid_time():
    """Тест корректных данных"""
    
    timer = TimerValidator(hh=10, mm=30, ss=15)
    assert timer.hh == 10
    assert timer.mm == 30
    assert timer.ss == 15


def test_not_int_type():
    """Тест исключения для некорректного типа данных"""
    
    with pytest.raises(TypeError) as excinfo:
        TimerValidator(hh="10", mm=30, ss=15)
    
    assert str(excinfo.value) == ErrorMessage.NOT_INT_TYPE.value


def test_no_time():
    """Тест исключения ситуации когда не указано время"""
    
    with pytest.raises(ValueError) as excinfo:
        TimerValidator(hh=0, mm=0, ss=0)
    
    assert str(excinfo.value) == ErrorMessage.NO_TIME.value


def test_negative_time():
    """Тест исключения для отрицательного времени"""
    
    with pytest.raises(ValueError) as excinfo:
        TimerValidator(hh=-1, mm=30, ss=15)
    
    assert str(excinfo.value) == ErrorMessage.NEGATIVE_TIME.value


def test_exceed_seconds_or_minutes():
    """Тест исключения для секунд/минут больше 59"""
    
    with pytest.raises(ValueError) as excinfo:
        TimerValidator(hh=0, mm=60, ss=10)
    
    assert str(excinfo.value) == ErrorMessage.SS_MM_BIG.value


def test_exceed_hours():
    """Тест исключения для часов больше 23"""
    
    with pytest.raises(ValueError) as excinfo:
        TimerValidator(hh=24, mm=0, ss=0)
    
    assert str(excinfo.value) == ErrorMessage.HH_BIG.value
