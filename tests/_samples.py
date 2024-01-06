"""
Содержит образцы текста для тестирования распознавания.
Для каждого образца должны быть указаны две вещи:
    1. Объект DateTimeObj, который должен быть получен в результате извлечения факта.
    2. Дата и время в ISO, полученные в результате привязки факта к моменту ORIGIN.
Для ситуаций, где время отсутствует, следует указывать время 00:00.
"""
from datetime import datetime

from date_extracting.facts import DateTimeObj, TimeSpecType
from date_extracting.binding import BindType


ORIGIN = datetime.fromisoformat("2023-12-30 14:00")
SAMPLES: dict[str, tuple[DateTimeObj, dict[BindType, str]]] = {
    "8 марта": (
        DateTimeObj(day=8, month=3),
        {
            BindType.FUTURE: "2024-03-08 00:00",
            BindType.PAST: "2023-03-08 00:00",
            BindType.CLOSEST: "2024-03-08 00:00",
        }
    ),
    "8е марта": (
        DateTimeObj(day=8, month=3),
        {
            BindType.FUTURE: "2024-03-08 00:00",
            BindType.PAST: "2023-03-08 00:00",
            BindType.CLOSEST: "2024-03-08 00:00",
        }
    ),
    "восьмое марта": (
        DateTimeObj(day=8, month=3),
        {
            BindType.FUTURE: "2024-03-08 00:00",
            BindType.PAST: "2023-03-08 00:00",
            BindType.CLOSEST: "2024-03-08 00:00",
        }
    ),
    "8.03": (
        DateTimeObj(day=8, month=3),
        {
            BindType.FUTURE: "2024-03-08 00:00",
            BindType.PAST: "2023-03-08 00:00",
            BindType.CLOSEST: "2024-03-08 00:00",
        }
    ),
    "08/03": (
        DateTimeObj(day=8, month=3),
        {
            BindType.FUTURE: "2024-03-08 00:00",
            BindType.PAST: "2023-03-08 00:00",
            BindType.CLOSEST: "2024-03-08 00:00",
        }
    ),
    "8 марта 2020 г.": (
        DateTimeObj(year=2020, day=8, month=3),
        {
            BindType.FUTURE: "2020-03-08 00:00",
            BindType.PAST: "2020-03-08 00:00",
            BindType.CLOSEST: "2020-03-08 00:00",
        }
    ),
    "08/03/2020": (
        DateTimeObj(year=2020, day=8, month=3),
        {
            BindType.FUTURE: "2020-03-08 00:00",
            BindType.PAST: "2020-03-08 00:00",
            BindType.CLOSEST: "2020-03-08 00:00",
        }
    ),
    "26 декабря 2023 в 11:00": (
        DateTimeObj(year=2023, month=12, day=26, hour=11, minute=0, spec=TimeSpecType.PRECISE),
        {
            BindType.FUTURE: "2023-12-26 11:00",
            BindType.PAST: "2023-12-26 11:00",
            BindType.CLOSEST: "2023-12-26 11:00",
        }
    ),
    "26 декабря 2023 11:00": (
        DateTimeObj(year=2023, month=12, day=26, hour=11, minute=0, spec=TimeSpecType.PRECISE),
        {
            BindType.FUTURE: "2023-12-26 11:00",
            BindType.PAST: "2023-12-26 11:00",
            BindType.CLOSEST: "2023-12-26 11:00",
        }
    ),
    "26-12-2023 в 11-00": (
        DateTimeObj(year=2023, month=12, day=26, hour=11, minute=0, spec=TimeSpecType.PRECISE),
        {
            BindType.FUTURE: "2023-12-26 11:00",
            BindType.PAST: "2023-12-26 11:00",
            BindType.CLOSEST: "2023-12-26 11:00",
        }
    ),
    "26го числа в час дня": (
        DateTimeObj(day=26, hour=1, spec=TimeSpecType.PM),
        {
            BindType.FUTURE: "2024-01-26 13:00",
            BindType.PAST: "2023-12-26 13:00",
            BindType.CLOSEST: "2023-12-26 13:00",
        }
    ),
    "третьего числа в девять утра": (
        DateTimeObj(day=3, hour=9, spec=TimeSpecType.AM),
        {
            BindType.FUTURE: "2024-01-03 09:00",
            BindType.PAST: "2023-12-03 09:00",
            BindType.CLOSEST: "2024-01-03 09:00",
        }
    ),
    "в четверг, в девять утра": (
        DateTimeObj(dow=3, hour=9, spec=TimeSpecType.AM),
        {
            BindType.FUTURE: "2024-01-04 09:00",
            BindType.PAST: "2023-12-28 09:00",
            BindType.CLOSEST: "2023-12-28 09:00",
        }
    ),
    "в четверг, 28.12.2023, в 10:00": (
        DateTimeObj(dow=3, day=28, month=12, year=2023, hour=10, minute=0, spec=TimeSpecType.PRECISE),
        {
            BindType.FUTURE: "2023-12-28 10:00",
            BindType.PAST: "2023-12-28 10:00",
            BindType.CLOSEST: "2023-12-28 10:00",
        }
    ),
    "завтра в десять утра": (
        DateTimeObj(day_delta=1, hour=10, spec=TimeSpecType.AM),
        {
            BindType.FUTURE: "2023-12-31 10:00",
            BindType.PAST: "2023-12-31 10:00",
            BindType.CLOSEST: "2023-12-31 10:00",
        }
    ),
    "завтра в полдень": (
        DateTimeObj(day_delta=1, hour=12, spec=None),
        {
            BindType.FUTURE: "2023-12-31 12:00",
            BindType.PAST: "2023-12-31 12:00",
            BindType.CLOSEST: "2023-12-31 12:00",
        }
    ),
    "позавчера": (
        DateTimeObj(day_delta=-2),
        {
            BindType.FUTURE: "2023-12-28 00:00",
            BindType.PAST: "2023-12-28 00:00",
            BindType.CLOSEST: "2023-12-28 00:00",
        }
    ),
    "вчера": (
        DateTimeObj(day_delta=-1),
        {
            BindType.FUTURE: "2023-12-29 00:00",
            BindType.PAST: "2023-12-29 00:00",
            BindType.CLOSEST: "2023-12-29 00:00",
        }
    ),
    "сегодня": (
        DateTimeObj(day_delta=0),
        {
            BindType.FUTURE: "2023-12-30 00:00",
            BindType.PAST: "2023-12-30 00:00",
            BindType.CLOSEST: "2023-12-30 00:00",
        }
    ),
    "завтра": (
        DateTimeObj(day_delta=1),
        {
            BindType.FUTURE: "2023-12-31 00:00",
            BindType.PAST: "2023-12-31 00:00",
            BindType.CLOSEST: "2023-12-31 00:00",
        }
    ),
    "послезавтра": (
        DateTimeObj(day_delta=2),
        {
            BindType.FUTURE: "2024-01-01 00:00",
            BindType.PAST: "2024-01-01 00:00",
            BindType.CLOSEST: "2024-01-01 00:00",
        }
    ),
    "через день": (
        DateTimeObj(day_delta=2),
        {
            BindType.FUTURE: "2024-01-01 00:00",
            BindType.PAST: "2024-01-01 00:00",
            BindType.CLOSEST: "2024-01-01 00:00",
        }
    ),  # 1
    "день тому назад": (
        DateTimeObj(day_delta=-2),
        {
            BindType.FUTURE: "2023-12-28 00:00",
            BindType.PAST: "2023-12-28 00:00",
            BindType.CLOSEST: "2023-12-28 00:00",
        }
    ),  # 1
    "через 2 дня": (
        DateTimeObj(day_delta=3),
        {
            BindType.FUTURE: "2024-01-02 00:00",
            BindType.PAST: "2024-01-02 00:00",
            BindType.CLOSEST: "2024-01-02 00:00",
        }
    ),  # 1
    "2 дня назад": (
        DateTimeObj(day_delta=-3),
        {
            BindType.FUTURE: "2023-12-27 00:00",
            BindType.PAST: "2023-12-27 00:00",
            BindType.CLOSEST: "2023-12-27 00:00",
        }
    ),  # 1
    "спустя трое суток": (
        DateTimeObj(day_delta=4),
        {
            BindType.FUTURE: "2024-01-03 00:00",
            BindType.PAST: "2024-01-03 00:00",
            BindType.CLOSEST: "2024-01-03 00:00",
        }
    ),  # 1
    "третьего числа": (
        DateTimeObj(day=3),
        {
            BindType.FUTURE: "2024-01-03 00:00",
            BindType.PAST: "2023-12-03 00:00",
            BindType.CLOSEST: "2024-01-03 00:00",
        }
    ),
    "третьего в 17-00": (
        DateTimeObj(day=3, hour=17, minute=0, spec=TimeSpecType.PRECISE),
        {
            BindType.FUTURE: "2024-01-03 17:00",
            BindType.PAST: "2023-12-03 17:00",
            BindType.CLOSEST: "2024-01-03 17:00",
        }
    ),
    "3 числа": (
        DateTimeObj(day=3),
        {
            BindType.FUTURE: "2024-01-03 00:00",
            BindType.PAST: "2023-12-03 00:00",
            BindType.CLOSEST: "2024-01-03 00:00",
        }
    ),
    "3го числа": (
        DateTimeObj(day=3),
        {
            BindType.FUTURE: "2024-01-03 00:00",
            BindType.PAST: "2023-12-03 00:00",
            BindType.CLOSEST: "2024-01-03 00:00",
        }
    ),
    "через неделю": (
        DateTimeObj(day_delta=7),
        {
            BindType.FUTURE: "2024-01-06 00:00",
            BindType.PAST: "2024-01-06 00:00",
            BindType.CLOSEST: "2024-01-06 00:00",
        }
    ),
    "неделю назад": (
        DateTimeObj(day_delta=-7),
        {
            BindType.FUTURE: "2023-12-23 00:00",
            BindType.PAST: "2023-12-23 00:00",
            BindType.CLOSEST: "2023-12-23 00:00",
        }
    ),
    "через 2 недели": (
        DateTimeObj(day_delta=14),
        {
            BindType.FUTURE: "2024-01-13 00:00",
            BindType.PAST: "2024-01-13 00:00",
            BindType.CLOSEST: "2024-01-13 00:00",
        }
    ),
    "2 недели тому назад": (
        DateTimeObj(day_delta=-14),
        {
            BindType.FUTURE: "2023-12-16 00:00",
            BindType.PAST: "2023-12-16 00:00",
            BindType.CLOSEST: "2023-12-16 00:00",
        }
    ),
    "спустя три недели": (
        DateTimeObj(day_delta=21),
        {
            BindType.FUTURE: "2024-01-20 00:00",
            BindType.PAST: "2024-01-20 00:00",
            BindType.CLOSEST: "2024-01-20 00:00",
        }
    ),
    "три недели назад": (
        DateTimeObj(day_delta=-21),
        {
            BindType.FUTURE: "2023-12-09 00:00",
            BindType.PAST: "2023-12-09 00:00",
            BindType.CLOSEST: "2023-12-09 00:00",
        }
    ),
    "через месяц": (
        DateTimeObj(month_delta=1),
        {
            BindType.FUTURE: "2024-01-30 00:00",
            BindType.PAST: "2024-01-30 00:00",
            BindType.CLOSEST: "2024-01-30 00:00",
        }
    ),
    "месяц назад": (
        DateTimeObj(month_delta=-1),
        {
            BindType.FUTURE: "2023-11-30 00:00",
            BindType.PAST: "2023-11-30 00:00",
            BindType.CLOSEST: "2023-11-30 00:00",
        }
    ),
    "через 2 месяца": (
        DateTimeObj(month_delta=2),
        {
            BindType.FUTURE: "2024-03-01 00:00",
            BindType.PAST: "2024-03-01 00:00",
            BindType.CLOSEST: "2024-03-01 00:00",
        }
    ),  # не бывает 02-30
    "2 месяца тому назад": (
        DateTimeObj(month_delta=-2),
        {
            BindType.FUTURE: "2023-10-30 00:00",
            BindType.PAST: "2023-10-30 00:00",
            BindType.CLOSEST: "2023-10-30 00:00",
        }
    ),
    "спустя три месяца": (
        DateTimeObj(month_delta=3),
        {
            BindType.FUTURE: "2024-03-30 00:00",
            BindType.PAST: "2024-03-30 00:00",
            BindType.CLOSEST: "2024-03-30 00:00",
        }
    ),
    "три месяца назад": (
        DateTimeObj(month_delta=-3),
        {
            BindType.FUTURE: "2023-09-30 00:00",
            BindType.PAST: "2023-09-30 00:00",
            BindType.CLOSEST: "2023-09-30 00:00",
        }
    ),
    "через пять минут": (
        DateTimeObj(minute_delta=5),
        {
            BindType.FUTURE: "2023-12-30 14:05",
            BindType.PAST: "2023-12-30 14:05",
            BindType.CLOSEST: "2023-12-30 14:05",
        }
    ),
    "пять минут назад": (
        DateTimeObj(minute_delta=-5),
        {
            BindType.FUTURE: "2023-12-30 13:55",
            BindType.PAST: "2023-12-30 13:55",
            BindType.CLOSEST: "2023-12-30 13:55",
        }
    ),
    "через час": (
        DateTimeObj(hour_delta=1),
        {
            BindType.FUTURE: "2023-12-30 15:00",
            BindType.PAST: "2023-12-30 15:00",
            BindType.CLOSEST: "2023-12-30 15:00",
        }
    ),
    "час назад": (
        DateTimeObj(hour_delta=-1),
        {
            BindType.FUTURE: "2023-12-30 13:00",
            BindType.PAST: "2023-12-30 13:00",
            BindType.CLOSEST: "2023-12-30 13:00",
        }
    ),
    "через 2 часа": (
        DateTimeObj(hour_delta=2),
        {
            BindType.FUTURE: "2023-12-30 16:00",
            BindType.PAST: "2023-12-30 16:00",
            BindType.CLOSEST: "2023-12-30 16:00",
        }
    ),
    "2 часа назад": (
        DateTimeObj(hour_delta=-2),
        {
            BindType.FUTURE: "2023-12-30 12:00",
            BindType.PAST: "2023-12-30 12:00",
            BindType.CLOSEST: "2023-12-30 12:00",
        }
    ),
    "спустя три часа": (
        DateTimeObj(hour_delta=3),
        {
            BindType.FUTURE: "2023-12-30 17:00",
            BindType.PAST: "2023-12-30 17:00",
            BindType.CLOSEST: "2023-12-30 17:00",
        }
    ),
    "три часа назад": (
        DateTimeObj(hour_delta=-3),
        {
            BindType.FUTURE: "2023-12-30 11:00",
            BindType.PAST: "2023-12-30 11:00",
            BindType.CLOSEST: "2023-12-30 11:00",
        }
    ),
    "через два с половиной часа": (
        DateTimeObj(hour_delta=2, minute_delta=30),
        {
            BindType.FUTURE: "2023-12-30 16:30",
            BindType.PAST: "2023-12-30 16:30",
            BindType.CLOSEST: "2023-12-30 16:30",
        }
    ),
    "два с половиной часа тому назад": (
        DateTimeObj(hour_delta=-2, minute_delta=-30),
        {
            BindType.FUTURE: "2023-12-30 11:30",
            BindType.PAST: "2023-12-30 11:30",
            BindType.CLOSEST: "2023-12-30 11:30",
        }
    ),
    "спустя 2 часа 30 минут": (
        DateTimeObj(hour_delta=2, minute_delta=30),
        {
            BindType.FUTURE: "2023-12-30 16:30",
            BindType.PAST: "2023-12-30 16:30",
            BindType.CLOSEST: "2023-12-30 16:30",
        }
    ),
    "2 часа 30 минут назад": (
        DateTimeObj(hour_delta=-2, minute_delta=-30),
        {
            BindType.FUTURE: "2023-12-30 11:30",
            BindType.PAST: "2023-12-30 11:30",
            BindType.CLOSEST: "2023-12-30 11:30",
        }
    ),
    "в час дня": (
        DateTimeObj(hour=1, spec=TimeSpecType.PM),
        {
            BindType.FUTURE: "2023-12-31 13:00",  # час дня уже прошел - это будет завтра
            BindType.PAST: "2023-12-30 13:00",  # час дня уже прошел - это было сегодня
            BindType.CLOSEST: "2023-12-30 13:00",
        }
    ),
    "в 2 часа дня": (
        DateTimeObj(hour=2, spec=TimeSpecType.PM),
        {
            BindType.FUTURE: "2023-12-31 14:00",  # уже два часа дня - это будет завтра
            BindType.PAST: "2023-12-30 14:00",  # сейчас два часа дня - это прямо сейчас
            BindType.CLOSEST: "2023-12-30 14:00",
        }
    ),
    "в два часа ночи": (
        DateTimeObj(hour=2, spec=TimeSpecType.AM),
        {
            BindType.FUTURE: "2023-12-31 02:00",  # два часа ночи уже прошли - это будет завтра
            BindType.PAST: "2023-12-30 02:00",  # два часа ночи уже прошли - это было сегодня
            BindType.CLOSEST: "2023-12-31 02:00",  # расстояние равное - предпочитаем будущее
        }
    ),
    "в 8 вечера": (
        DateTimeObj(hour=8, spec=TimeSpecType.PM),
        {
            BindType.FUTURE: "2023-12-30 20:00",  # сегодня 8 вечера ещё не было - сегодня
            BindType.PAST: "2023-12-29 20:00",  # сегодня 8 вечера ещё не было - вчера
            BindType.CLOSEST: "2023-12-30 20:00",
        }
    ),
    "8 вечера": (
        DateTimeObj(hour=8, spec=TimeSpecType.PM),
        {
            BindType.FUTURE: "2023-12-30 20:00",  # сегодня 8 вечера ещё не было - сегодня
            BindType.PAST: "2023-12-29 20:00",  # сегодня 8 вечера ещё не было - вчера
            BindType.CLOSEST: "2023-12-30 20:00",
        }
    ),
    "в шесть утра": (
        DateTimeObj(hour=6, spec=TimeSpecType.AM),
        {
            BindType.FUTURE: "2023-12-31 06:00",  # сегодня 6 утра уже было - завтра
            BindType.PAST: "2023-12-30 06:00",  # сегодня 6 утра уже было - сегодня
            BindType.CLOSEST: "2023-12-30 06:00",
        }
    ),
    "в шесть часов утра": (
        DateTimeObj(hour=6, spec=TimeSpecType.AM),
        {
            BindType.FUTURE: "2023-12-31 06:00",  # сегодня 6 утра уже было - завтра
            BindType.PAST: "2023-12-30 06:00",  # сегодня 6 утра уже было - сегодня
            BindType.CLOSEST: "2023-12-30 06:00",
        }
    ),
    "в 14 часов": (
        DateTimeObj(hour=14, spec=None),
        {
            BindType.FUTURE: "2023-12-31 14:00",  # сейчас уже 14 часов - это будет завтра
            BindType.PAST: "2023-12-30 14:00",  # сейчас уже 14 часов - это прямо сейчас
            BindType.CLOSEST: "2023-12-30 14:00",
        }
    ),
    "в 14 часов 30 минут": (
        DateTimeObj(hour=14, minute=30, spec=None),
        {
            BindType.FUTURE: "2023-12-30 14:30",  # сейчас ещё два часа дня - это будет сегодня
            BindType.PAST: "2023-12-29 14:30",  # сейчас ещё два часа дня - это было вчера
            BindType.CLOSEST: "2023-12-30 14:30",
        }
    ),
    "в 20 минут": (
        DateTimeObj(minute=20, spec=None),
        {
            BindType.FUTURE: "2023-12-30 14:20",  # сейчас 00 минут - этот час
            BindType.PAST: "2023-12-30 13:20",  # сейчас 00 минут - предыдущий час
            BindType.CLOSEST: "2023-12-30 14:20",
        }
    ),
    "в 20 минут шестого": (
        DateTimeObj(hour=5, minute=20, spec=None),
        {
            BindType.FUTURE: "2023-12-30 17:20",
            BindType.PAST: "2023-12-29 17:20",
            BindType.CLOSEST: "2023-12-30 17:20",
        }
    ),
    "в половину шестого": (
        DateTimeObj(hour=5, minute=30, spec=None),
        {
            BindType.FUTURE: "2023-12-30 17:30",
            BindType.PAST: "2023-12-29 17:30",
            BindType.CLOSEST: "2023-12-30 17:30",
        }
    ),
    "в пол-шестого": (
        DateTimeObj(hour=5, minute=30, spec=None),
        {
            BindType.FUTURE: "2023-12-30 17:30",
            BindType.PAST: "2023-12-29 17:30",
            BindType.CLOSEST: "2023-12-30 17:30",
        }
    ),
    "в без пятнадцати шесть": (
        DateTimeObj(hour=5, minute=45, spec=None),
        {
            BindType.FUTURE: "2023-12-30 17:45",
            BindType.PAST: "2023-12-29 17:45",
            BindType.CLOSEST: "2023-12-30 17:45",
        }
    ),
    "в без десяти 8": (
        DateTimeObj(hour=7, minute=50, spec=None),
        {
            BindType.FUTURE: "2023-12-30 19:50",
            BindType.PAST: "2023-12-29 19:50",
            BindType.CLOSEST: "2023-12-30 19:50",
        }
    ),
    "в без двадцати час": (
        DateTimeObj(hour=12, minute=40, spec=None),
        {
            BindType.FUTURE: "2023-12-31 12:40",  # 12:40 сегодня уже было - завтра
            BindType.PAST: "2023-12-30 12:40",  # 12:40 сегодня уже было - сегодня
            BindType.CLOSEST: "2023-12-30 12:40",
        }
    ),
    "в без двадцати пяти час": (
        DateTimeObj(hour=12, minute=35, spec=None),
        {
            BindType.FUTURE: "2023-12-31 12:35",  # 12:35 сегодня уже было - завтра
            BindType.PAST: "2023-12-30 12:35",  # 12:35 сегодня уже было - сегодня
            BindType.CLOSEST: "2023-12-30 12:35",
        }
    ),
    "в без двадцати пяти минут час": (
        DateTimeObj(hour=12, minute=35, spec=None),
        {
            BindType.FUTURE: "2023-12-31 12:35",  # 12:35 сегодня уже было - завтра
            BindType.PAST: "2023-12-30 12:35",  # 12:35 сегодня уже было - сегодня
            BindType.CLOSEST: "2023-12-30 12:35",
        }
    ),
    "в без двадцати пять часов": (
        DateTimeObj(hour=4, minute=40, spec=None),
        {
            BindType.FUTURE: "2023-12-30 16:40",  # 16:40 сегодня ещё не было - сегодня
            BindType.PAST: "2023-12-29 16:40",  # 16:40 сегодня ещё не было - вчера
            BindType.CLOSEST: "2023-12-30 16:40",
        }
    ),
    "в 14:30": (
        DateTimeObj(hour=14, minute=30, spec=TimeSpecType.PRECISE),
        {
            BindType.FUTURE: "2023-12-30 14:30",  # сейчас ещё два часа дня - это будет сегодня
            BindType.PAST: "2023-12-29 14:30",  # сейчас ещё два часа дня - это было вчера
            BindType.CLOSEST: "2023-12-30 14:30",
        }
    ),
    "в 14-30": (
        DateTimeObj(hour=14, minute=30, spec=TimeSpecType.PRECISE),
        {
            BindType.FUTURE: "2023-12-30 14:30",  # сейчас ещё два часа дня - это будет сегодня
            BindType.PAST: "2023-12-29 14:30",  # сейчас ещё два часа дня - это было вчера
            BindType.CLOSEST: "2023-12-30 14:30",
        }
    ),
    "в полдень": (
        DateTimeObj(hour=12, spec=None),
        {
            BindType.FUTURE: "2023-12-31 12:00",  # 12:00 сегодня уже было - завтра
            BindType.PAST: "2023-12-30 12:00",  # 12:00 сегодня уже было - сегодня
            BindType.CLOSEST: "2023-12-30 12:00",
        }
    ),
    "в полночь": (
        DateTimeObj(hour=0, spec=None),
        {
            BindType.FUTURE: "2023-12-31 00:00",  # 00:00 сегодня уже было - завтра
            BindType.PAST: "2023-12-30 00:00",  # 00:00 сегодня уже было - сегодня
            BindType.CLOSEST: "2023-12-31 00:00",  # после полудня - следующая полночь ближе
        }
    ),
    "во вторник": (
        DateTimeObj(week=None, dow=1),
        {
            BindType.FUTURE: "2024-01-02 00:00",
            BindType.PAST: "2023-12-26 00:00",
            BindType.CLOSEST: "2024-01-02 00:00",
        }
    ),
    "в пятницу": (
        DateTimeObj(week=None, dow=4),
        {
            BindType.FUTURE: "2024-01-05 00:00",
            BindType.PAST: "2023-12-29 00:00",
            BindType.CLOSEST: "2023-12-29 00:00",
        }
    ),
    "в этот вторник": (
        DateTimeObj(week=0, dow=1),
        {
            BindType.FUTURE: "2023-12-26 00:00",
            BindType.PAST: "2023-12-26 00:00",
            BindType.CLOSEST: "2023-12-26 00:00",
        }
    ),
    "в эту пятницу": (
        DateTimeObj(week=0, dow=4),
        {
            BindType.FUTURE: "2023-12-29 00:00",
            BindType.PAST: "2023-12-29 00:00",
            BindType.CLOSEST: "2023-12-29 00:00",
        }
    ),
    "в прошлый вторник": (
        DateTimeObj(week=-1, dow=1),
        {
            BindType.FUTURE: "2023-12-19 00:00",
            BindType.PAST: "2023-12-19 00:00",
            BindType.CLOSEST: "2023-12-19 00:00",
        }
    ),
    "в ту пятницу": (
        DateTimeObj(week=-1, dow=4),
        {
            BindType.FUTURE: "2023-12-22 00:00",
            BindType.PAST: "2023-12-22 00:00",
            BindType.CLOSEST: "2023-12-22 00:00",
        }
    ),
    "в следующий вторник": (
        DateTimeObj(week=1, dow=1),
        {
            BindType.FUTURE: "2024-01-02 00:00",
            BindType.PAST: "2024-01-02 00:00",
            BindType.CLOSEST: "2024-01-02 00:00",
        }
    ),
    "в следующую пятницу": (
        DateTimeObj(week=1, dow=4),
        {
            BindType.FUTURE: "2024-01-05 00:00",
            BindType.PAST: "2024-01-05 00:00",
            BindType.CLOSEST: "2024-01-05 00:00",
        }
    ),
    "2020": (
        DateTimeObj(year=2020),
        {
            BindType.FUTURE: "2020-12-30 00:00",
            BindType.PAST: "2020-12-30 00:00",
            BindType.CLOSEST: "2020-12-30 00:00",
        }
    ),
    "2020 года": (
        DateTimeObj(year=2020),
        {
            BindType.FUTURE: "2020-12-30 00:00",
            BindType.PAST: "2020-12-30 00:00",
            BindType.CLOSEST: "2020-12-30 00:00",
        }
    ),
    "2020 г.": (
        DateTimeObj(year=2020),
        {
            BindType.FUTURE: "2020-12-30 00:00",
            BindType.PAST: "2020-12-30 00:00",
            BindType.CLOSEST: "2020-12-30 00:00",
        }
    ),
    "февраль 2024": (
        DateTimeObj(year=2024, month=2),
        {
            BindType.FUTURE: "2024-02-28 00:00",
            BindType.PAST: "2024-02-28 00:00",
            BindType.CLOSEST: "2024-02-28 00:00",
        }
    ),  # 30е число не во всех месяцах, максимум 28е
    "через год": (
        DateTimeObj(year_delta=1),
        {
            BindType.FUTURE: "2024-12-30 00:00",
            BindType.PAST: "2024-12-30 00:00",
            BindType.CLOSEST: "2024-12-30 00:00",
        }
    ),
    "год назад": (
        DateTimeObj(year_delta=-1),
        {
            BindType.FUTURE: "2022-12-30 00:00",
            BindType.PAST: "2022-12-30 00:00",
            BindType.CLOSEST: "2022-12-30 00:00",
        }
    ),
    "через 5 лет": (
        DateTimeObj(year_delta=5),
        {
            BindType.FUTURE: "2028-12-30 00:00",
            BindType.PAST: "2028-12-30 00:00",
            BindType.CLOSEST: "2028-12-30 00:00",
        }
    ),
    "5 лет назад": (
        DateTimeObj(year_delta=-5),
        {
            BindType.FUTURE: "2018-12-30 00:00",
            BindType.PAST: "2018-12-30 00:00",
            BindType.CLOSEST: "2018-12-30 00:00",
        }
    ),
    "спустя три года": (
        DateTimeObj(year_delta=3),
        {
            BindType.FUTURE: "2026-12-30 00:00",
            BindType.PAST: "2026-12-30 00:00",
            BindType.CLOSEST: "2026-12-30 00:00",
        }
    ),
    "три года тому назад": (
        DateTimeObj(year_delta=-3),
        {
            BindType.FUTURE: "2020-12-30 00:00",
            BindType.PAST: "2020-12-30 00:00",
            BindType.CLOSEST: "2020-12-30 00:00",
        }
    ),
    "через год, 2 месяца, 3 дня и 12 часов": (
        DateTimeObj(year_delta=1, month_delta=2, day_delta=4, hour_delta=12),
        {
            BindType.FUTURE: "2025-03-06 02:00",
            BindType.PAST: "2025-03-06 02:00",
            BindType.CLOSEST: "2025-03-06 02:00",
        }
    ),  # 1
    "год, 2 месяца, 3 дня и 12 часов назад": (
        DateTimeObj(year_delta=-1, month_delta=-2, day_delta=-4, hour_delta=-12),
        {
            BindType.FUTURE: "2022-10-26 02:00",
            BindType.PAST: "2022-10-26 02:00",
            BindType.CLOSEST: "2022-10-26 02:00",
        }
    ),  # 1
}
# [1] Через день = сегодня -> пропускаем день -> целевой день. Так что к указанному в тексте числу дней добавляем 1.
