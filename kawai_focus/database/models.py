from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String

from kawai_focus.database.mixins import IDMixin


class Base(DeclarativeBase):
    """Класс для корректной работы аннотаций"""

    pass


class Timer(IDMixin, Base):
    """Модель таймера"""

    __tablename__ = 'timer'

    title: Mapped[str] = mapped_column(
        String(length=200),
        name='название',
        nullable=False
    )

    pomodoro_time: Mapped[int] = mapped_column(
        Integer,
        name='время помидора',
        nullable=False
    )

    break_time: Mapped[int] = mapped_column(
        Integer,
        name='время перерыва',
        nullable=False
    )

    break_long_time: Mapped[int] = mapped_column(
        Integer,
        name='время долгого перерыва',
        nullable=False
    )

    count_pomodoro: Mapped[int] = mapped_column(
        Integer,
        name='количество помидоров',
        nullable=False
    )
