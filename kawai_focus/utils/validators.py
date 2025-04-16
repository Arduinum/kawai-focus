from dataclasses import dataclass
from kawai_focus.utils.errors import ErrorMessage 


@dataclass
class TimerValidator:
    """Класс для валидации функции таймера."""

    hh: int = 0
    mm: int = 0
    ss: int = 0

    def __post_init__(self):
        if not all(isinstance(value, int) for value in (self.hh, self.mm, self.ss)):
            raise TypeError(ErrorMessage.NOT_INT_TYPE.value)

        if self.ss == 0 and self.mm == 0 and self.hh == 0:
            raise ValueError(ErrorMessage.NO_TIME.value)
        
        if self.ss < 0 or self.mm < 0 or self.hh < 0:
            raise ValueError(ErrorMessage.NEGATIVE_TIME.value)

        if self.ss > 59 or self.mm > 59:
            raise ValueError(ErrorMessage.SS_MM_BIG.value)
        
        if self.hh > 23:
            raise ValueError(ErrorMessage.HH_BIG.value)

