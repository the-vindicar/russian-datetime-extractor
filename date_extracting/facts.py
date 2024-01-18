"""Содержит описания факта о дате/времени, извлечённого из текста,
а также вспомогательных классов."""
from typing import Optional
import enum

from yargy.interpretation import fact
from natasha import obj

__all__ = ['DateTimeFact', 'DateTimeObj', 'TimeSpecType']


class TimeSpecType(enum.Enum):
    """Способ, которым задано время:
        - PRECISE - время задано точно: "11:00"
        - AM - время задано как утро или ночь: "6 утра", "два часа ночи"
        - PM - время задано как день или вечер: "два часа дня", "6 вечера"
    """
    PRECISE = 2
    AM = 3
    PM = 4


class DateTimeObj(obj.Obj):
    """Факт о дате и времени, содержащий сведения о характере и сути описания момента времени.
    Любое из нижеперечисленных полей может быть None, если соответствующий элемент отсутствовал в описании.

    Attributes:

    year - абсолютное значение года.
    month - абсолютное значение месяца (номер 1-12).
    day - абсолютное значение дня (1-31).
    week - указание на неделю при задании дня недели.
        - -1 - прошлая
        - 0 - текущая
        - 1 - следующая
        - None - не указано.
    dow - указание на день недели (0-6, где 0 - понедельник)
    hour - абсолютное значение часа (0-23).
    minute - абсолютное значение минут (0-59).
    spec - указание на тип задания времени. См. перечисление TimeSpecType.
        - AM - ночь/утро
        - PM - день/вечер
        - PRECISE - время задано точно, в виде "9:00" или похожем
        - не задано (None) - указание неоднозначно ("в два часа").
    year_delta - смещение по годам ("спустя год").
    month_delta - смещение по месяцам.
    day_delta - смещение по дням.
    hour_delta - смещение по часам.
    minute_delta - смещение по минутам.
    """
    __attributes__ = [
        'year', 'month', 'day',
        'week', 'dow',
        'hour', 'minute', 'spec',
        'year_delta', 'month_delta', 'day_delta',
        'hour_delta', 'minute_delta'
    ]

    year: Optional[int]
    month: Optional[int]
    day: Optional[int]
    week: Optional[int]
    dow: Optional[int]
    hour: Optional[int]
    minute: Optional[int]
    spec: Optional[TimeSpecType]
    year_delta: Optional[int]
    month_delta: Optional[int]
    day_delta: Optional[int]
    hour_delta: Optional[int]
    minute_delta: Optional[int]

    @property
    def has_delta(self) -> bool:
        """Возвращает True, если факт содержит относительные указания на дату и/или время."""
        values = (self.year_delta, self.month_delta, self.day_delta, self.dow,
                  self.hour_delta, self.minute_delta)
        return any(v is not None for v in values)

    @property
    def has_date(self) -> bool:
        """Возвращает True, если факт содержит абсолютное или относительное указание на дату."""
        values = (self.year_delta, self.month_delta, self.day_delta, self.dow,
                  self.year, self.month, self.day)
        return any(v is not None for v in values)

    @property
    def has_time(self) -> bool:
        """Возвращает True, если факт содержит абсолютное или относительное указание на время."""
        values = (self.hour_delta, self.minute_delta, self.hour, self.minute)
        return any(d is not None for d in values)


class DateTimeFact(fact('DateTimeFact', DateTimeObj.__attributes__)):
    @property
    def obj(self):
        return DateTimeObj(
            **{a: getattr(self, a) for a in DateTimeObj.__attributes__}
        )
