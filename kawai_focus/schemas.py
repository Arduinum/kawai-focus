from pydantic import BaseModel, field_validator, Field
from kawai_focus.utils.errors import ErrorMessage 


class TimerModel(BaseModel):
    """Модель для валидации данных таймера"""

    id: int | None = None
    title: str
    pomodoro_time: int
    break_time: int
    break_long_time: int
    count_pomodoro: int


class TimerTimeModel(BaseModel):
    """Модель для валидации времени таймера"""

    hh: int = Field(0, ge=0, le=23)
    mm: int = Field(0, ge=0, le=59)
    ss: int = Field(0, ge=0, le=59)

    @field_validator('hh', 'mm', 'ss')
    @classmethod
    def check_all_time_fields(cls, value: int) -> int:
        """Метод валидирует все поля времени"""

        # гарантирует, что время не равно 00:00:00
        if value == 0:
            raise ValueError(ErrorMessage.NO_TIME.value)
    
        return value
