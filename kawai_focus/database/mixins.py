from sqlalchemy.orm import Mapped, mapped_column  
from sqlalchemy import Integer


class IDMixin:
    """Базовый класс для моделей с id"""

    id: Mapped[int] = mapped_column(
        Integer,
        name='id',
        primary_key=True,
        autoincrement=True
    )
