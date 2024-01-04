"""Реализует процесс "подгонки" извлечённого факта к выбранной точке отсчёта во времени."""
import typing as tp
from datetime import datetime, timedelta
from .facts import DateTimeObj, TimeSpecType


def bind_reference(fact: DateTimeObj, origin: datetime) -> tp.Tuple[datetime, bool]:
    """
    Преобразует извлечённый факт в описание даты и (опционально) времени c учётом
    заданной точки отсчёта. При неоднозначном указании (например, только число)
    ищет подходящую дату/время в будущем, а не в прошлом.

    :param fact: Описание факта, извлечённого из текста на естественном языке.
    :param origin: Точка отсчёта времени для неполных или относительных описаний ("пятого числа", "через час").
    :raises ValueError: Если полученный факт невозможно интерпретировать однозначно.
    :return: Точное указание на дату/время, а также флаг наличия времени.
    """
    year = origin.year
    month = origin.month
    day = origin.day
    hour = origin.hour
    minute = origin.minute
    if fact.has_delta:
        # было задано хотя бы одно относительное значение - учитываем их
        dyear: int = fact.year_delta or 0
        dmonth: int = fact.month_delta or 0
        try:
            target: datetime = origin.replace(
                year=origin.year + dyear + (1 if (dmonth + origin.month) > 12 else 0),
                month=(origin.month - 1 + dmonth) % 12 + 1
            )
        except ValueError:  # 31 января + через месяц = ~1 марта а не 31 февраля
            target: datetime = origin.replace(
                year=origin.year + dyear + (1 if (dmonth + origin.month) > 12 else 0),
                month=(origin.month - 1 + dmonth + 1) % 12 + 1,
                day=1
            )

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
        else:  #есть указание на день, или ни на то ни на другое
            target = target + timedelta(days=fact.day_delta or 0)
        target = target + timedelta(
            hours=fact.hour_delta or 0,
            minutes=fact.minute_delta or 0
        )
        year = target.year
        month = target.month
        day = target.day
        hour = target.hour
        minute = target.minute
    # теперь пытаемся использовать абсолютные значения даты, если они есть
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
    # разбираемся со временем
    if fact.minute is not None and fact.hour is None:  # заданы минуты, но не час
        target = datetime(year=year, month=month, day=day, hour=origin.hour, minute=fact.minute)
        if fact.minute < origin.minute:  # минуты меньше текущих - должен быть следующий час
            target += timedelta(hours=1)
        year = target.year
        month = target.month
        day = target.day
        hour = target.hour
        minute = target.minute
    elif fact.hour is not None:  # задан хотя бы час
        if fact.spec == TimeSpecType.PRECISE:  # время задано точно, как 5:43
            hour = fact.hour
            minute = fact.minute or 0
        elif fact.spec == TimeSpecType.AM:  # "в N часов ночи/утра"
            hour = fact.hour
            minute = fact.minute or 0
        elif fact.spec == TimeSpecType.PM:  # "в N часов дня/вечера"
            hour = (fact.hour + 12) if (fact.hour < 12) else fact.hour
            minute = fact.minute or 0
        else:  # fact.spec == None:  # требуется уточнение
            # всё что от 1 до 8 часов включительно - день и вечер.
            # всё остальное - утро (10 часов), или явно заданный час (0 часов, 14 часов)
            hour = (fact.hour + 12) if 1 <= fact.hour <= 8 else fact.hour
            minute = fact.minute or 0
        if not fact.has_date and (hour*60+minute) <= (origin.hour*60 + origin.minute):
            # планируем на время, меньшее или равное текущему - но при этом дата не указана
            # считаем,что это план на завтра
            target = datetime(year=year, month=month, day=day, hour=hour, minute=fact.minute or 0)
            target += timedelta(days=1)
            year = target.year
            month = target.month
            day = target.day
            hour = target.hour
            minute = target.minute
    if not fact.has_time:
        hour = 0
        minute = 0
    target = datetime(year=year, month=month, day=day, hour=hour, minute=minute)
    return target, fact.has_time
