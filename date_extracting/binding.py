"""Реализует процесс "подгонки" извлечённого факта к выбранной точке отсчёта во времени."""
import typing as tp
from datetime import datetime, timedelta
import enum
from .facts import DateTimeObj, TimeSpecType


class BindType(enum.Enum):
    PAST = -1
    CLOSEST = 0
    FUTURE = 1

def bind_reference(fact: DateTimeObj, direction: BindType, origin: datetime) -> tp.Tuple[datetime, bool]:
    """
    Преобразует извлечённый факт в описание даты и (опционально) времени c учётом
    заданной точки отсчёта. При неоднозначном указании (например, только число)
    ищет подходящую дату/время в будущем, а не в прошлом.

    :param fact: Описание факта, извлечённого из текста на естественном языке.
    :param direction: В каком направлении следует искать подходящую дату для неоднозначных описаний.
    :param origin: Точка отсчёта времени для неполных или относительных описаний ("пятого числа", "через час").
    :raises ValueError: Если полученный факт невозможно интерпретировать однозначно.
    :return: Точное указание на дату/время, а также флаг наличия времени.
    """
    target = origin
    if direction == BindType.FUTURE:
        if fact.has_delta:
            # было задано хотя бы одно относительное значение - учитываем их
            target = _bind_relative_future(fact, origin)
        # теперь пытаемся использовать абсолютные значения даты, если они есть
        target = _bind_absolute_date_future(fact, origin, target)
        # разбираемся со временем
        target = _bind_absolute_time_future(fact, origin, target)
    elif direction == BindType.PAST:
        if fact.has_delta:
            # было задано хотя бы одно относительное значение - учитываем их
            target = _bind_relative_past(fact, origin)
        # теперь пытаемся использовать абсолютные значения даты, если они есть
        target = _bind_absolute_date_past(fact, origin, target)
        # разбираемся со временем
        target = _bind_absolute_time_past(fact, origin, target)
    else:
        future, _ = bind_reference(fact, BindType.FUTURE, origin)
        past, _ = bind_reference(fact, BindType.PAST, origin)
        target = min([future, past], key=lambda dt: abs((dt - origin).total_seconds()))
    if not fact.has_time:
        target = target.replace(hour=0, minute=0)
    return target, fact.has_time


def _bind_absolute_time_future(fact: DateTimeObj, origin: datetime, target: datetime) -> datetime:
    """Учитывает абсолютные значения времени, если они заданы, с прицелом на будущее."""
    if fact.minute is not None and fact.hour is None:  # заданы минуты, но не час
        target = target.replace(hour=origin.hour, minute=fact.minute)
        if fact.minute < origin.minute:  # минуты меньше текущих - должен быть следующий час
            target += timedelta(hours=1)
    elif fact.hour is not None:  # задан хотя бы час
        if fact.spec == TimeSpecType.PRECISE:  # время задано точно, как 5:43
            target = target.replace(hour=fact.hour, minute=fact.minute or 0)
        elif fact.spec == TimeSpecType.AM:  # "в N часов ночи/утра"
            target = target.replace(hour=fact.hour, minute=fact.minute or 0)
        elif fact.spec == TimeSpecType.PM:  # "в N часов дня/вечера"
            target = target.replace(
                hour=(fact.hour + 12) if (fact.hour < 12) else fact.hour,
                minute=fact.minute or 0
            )
        else:  # fact.spec == None:  # требуется уточнение
            # всё что от 1 до 8 часов включительно - день и вечер.
            # всё остальное - утро (10 часов), или явно заданный час (0 часов, 14 часов)
            target = target.replace(
                hour=(fact.hour + 12) if 1 <= fact.hour <= 8 else fact.hour,
                minute=fact.minute or 0
            )
        if not fact.has_date and (target.hour * 60 + target.minute) <= (origin.hour * 60 + origin.minute):
            # планируем на время, меньшее или равное текущему - но при этом дата не указана
            # считаем,что это план на завтра
            target += timedelta(days=1)
    return target


def _bind_absolute_time_past(fact: DateTimeObj, origin: datetime, target: datetime) -> datetime:
    """Учитывает абсолютные значения времени, если они заданы, с прицелом на прошлое."""
    if fact.minute is not None and fact.hour is None:  # заданы минуты, но не час
        target = target.replace(hour=origin.hour, minute=fact.minute)
        if fact.minute > origin.minute:  # минуты больше текущих - должен быть предыдущий час
            target -= timedelta(hours=1)
    elif fact.hour is not None:  # задан хотя бы час
        if fact.spec == TimeSpecType.PRECISE:  # время задано точно, как 5:43
            target = target.replace(hour=fact.hour, minute=fact.minute or 0)
        elif fact.spec == TimeSpecType.AM:  # "в N часов ночи/утра"
            target = target.replace(hour=fact.hour, minute=fact.minute or 0)
        elif fact.spec == TimeSpecType.PM:  # "в N часов дня/вечера"
            target = target.replace(
                hour=(fact.hour + 12) if (fact.hour < 12) else fact.hour,
                minute=fact.minute or 0
            )
        else:  # fact.spec == None:  # требуется уточнение
            # всё что от 1 до 8 часов включительно - день и вечер.
            # всё остальное - утро (10 часов), или явно заданный час (0 часов, 14 часов)
            target = target.replace(
                hour=(fact.hour + 12) if 1 <= fact.hour <= 8 else fact.hour,
                minute=fact.minute or 0
            )
        if not fact.has_date and (target.hour * 60 + target.minute) > (origin.hour * 60 + origin.minute):
            # видим время, большее текущего - но при этом дата не указана
            # считаем,что это указание на вчерашний день
            target -= timedelta(days=1)
    return target


def _bind_absolute_date_future(fact: DateTimeObj, origin: datetime, target: datetime) -> datetime:
    """Учитывает абсолютные значения даты, если они заданы, с прицелом на будущее."""
    year = target.year
    month = target.month
    day = target.day
    hour = target.hour
    minute = target.minute
    if not fact.day and (fact.month or fact.year):  # не указан день, но есь месяц или год
        day = min(day, 28) if fact.month else day
        month = fact.month or month
        year = fact.year or year
    elif fact.day and not fact.month and not fact.year:  # задан только день
        if fact.day < origin.day:  # число меньше сегодняшнего - это должен быть следующий месяц
            if month < 12:
                month = origin.month + 1
            else:
                month = 1
                year = origin.year + 1
        day = fact.day
    elif fact.day and fact.month and not fact.year:  # задан день и месяц
        if (fact.month < origin.month) or (fact.month == origin.month and fact.day < origin.day):
            # месяц меньше текущего - должен быть следующий год
            year = origin.year + 1
        day = fact.day
        month = fact.month
    elif fact.day and fact.month and fact.year:  # дата задана полностью
        day = fact.day
        month = fact.month
        year = fact.year
    return datetime(year=year, month=month, day=day, hour=hour, minute=minute)


def _bind_absolute_date_past(fact: DateTimeObj, origin: datetime, target: datetime) -> datetime:
    """Учитывает абсолютные значения даты, если они заданы, с прицелом на прошлое."""
    year = target.year
    month = target.month
    day = target.day
    hour = target.hour
    minute = target.minute
    if not fact.day and (fact.month or fact.year):  # не указан день, но есть месяц или год
        day = min(day, 28) if fact.month else day
        month = fact.month or month
        year = fact.year or year
    elif fact.day and not fact.month and not fact.year:  # задан только день
        if fact.day > origin.day:  # число больше сегодняшнего - это должен быть предыдущий месяц
            if month > 1:
                month = origin.month + 1
            else:
                month = 12
                year = origin.year - 1
        day = fact.day
    elif fact.day and fact.month and not fact.year:  # задан день и месяц
        if (fact.month > origin.month) or (fact.month == origin.month and fact.day > origin.day):
            # месяц больше текущего - должен быть предыдущий год
            year = origin.year - 1
        day = fact.day
        month = fact.month
    elif fact.day and fact.month and fact.year:  # дата задана полностью
        day = fact.day
        month = fact.month
        year = fact.year
    return datetime(year=year, month=month, day=day, hour=hour, minute=minute)


def _bind_relative(fact: DateTimeObj, origin: datetime) -> datetime:
    dyear: int = fact.year_delta or 0
    dmonth: int = fact.month_delta or 0
    try:
        target: datetime = origin.replace(
            year=origin.year + dyear + (dmonth + origin.month - 1) // 12,
            month=(dmonth + origin.month - 1 + 12) % 12 + 1
        )
    except ValueError:  # 31 января + через месяц = ~1 марта а не 31 февраля
        target: datetime = origin.replace(
            year=origin.year + dyear + (dmonth + origin.month - 1) // 12,
            month=(origin.month - 1 + dmonth + 12) % 12 + 2,
            day=1
        )
    target = target + timedelta(
        hours=fact.hour_delta or 0,
        minutes=fact.minute_delta or 0
    )
    return target

def _bind_relative_future(fact: DateTimeObj, origin: datetime) -> datetime:
    """Выполняет расчёт относительно указанного времени с прицелом на будущее."""
    target = _bind_relative(fact, origin)
    if not fact.day_delta and fact.dow:
        # есть указание на день недели, но не на день
        if fact.week is None:  # неделя не указана - ищем с завтрашнего дня
            target = target + timedelta(days=1)
        else:  # неделя указана - ищем с понедельника этой недели
            while target.weekday() > 0:
                target -= timedelta(days=1)
            target = target + timedelta(weeks=fact.week)
        for _ in range(8):  # ищем день, приходящийся на нужный день недели
            if target.weekday() == fact.dow:
                break
            else:
                target += timedelta(days=1)
        else:
            raise ValueError('Impossible dow value!')
    else:  # есть указание на день, или ни на то ни на другое
        target = target + timedelta(days=fact.day_delta or 0)
    return target


def _bind_relative_past(fact: DateTimeObj, origin: datetime) -> datetime:
    """Выполняет расчёт относительно указанного времени с прицелом на прошлое."""
    target = _bind_relative(fact, origin)
    if not fact.day_delta and fact.dow:
        # есть указание на день недели, но не на день
        if fact.week is None:  # неделя не указана - ищем с вчерашнего дня
            target = target + timedelta(days=-1)
        else:  # неделя указана - ищем с воскресенья этой недели
            while target.weekday() < 6:
                target += timedelta(days=1)
            target = target + timedelta(weeks=fact.week)
        for _ in range(8):  # ищем день, приходящийся на нужный день недели
            if target.weekday() == fact.dow:
                break
            else:
                target -= timedelta(days=1)
        else:
            raise ValueError('Impossible dow value!')
    else:  # есть указание на день, или ни на то ни на другое
        target = target + timedelta(days=fact.day_delta or 0)
    return target
