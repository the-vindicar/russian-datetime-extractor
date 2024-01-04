"""
Содержит образцы текста для тестирования распознавания.
Для каждого образца должны быть указаны две вещи:
    1. Объект DateTimeObj, который должен быть получен в результате извлечения факта.
    2. Дата и время в ISO, полученные в результате привязки факта к моменту ORIGIN.
Для ситуаций, где время отсутствует, следует указывать время 00:00.
"""
from datetime import datetime

from date_extracting.facts import DateTimeObj, TimeSpecType

ORIGIN = datetime.fromisoformat("2023-12-30 14:00")
SAMPLES: dict[str, tuple[DateTimeObj, str]] = {
    "8 марта": (DateTimeObj(day=8, month=3), "2024-03-08 00:00"),
    "8е марта": (DateTimeObj(day=8, month=3), "2024-03-08 00:00"),
    "восьмое марта": (DateTimeObj(day=8, month=3), "2024-03-08 00:00"),
    "8.03": (DateTimeObj(day=8, month=3), "2024-03-08 00:00"),
    "08/03": (DateTimeObj(day=8, month=3), "2024-03-08 00:00"),
    "8 марта 2020 г.": (DateTimeObj(year=2020, day=8, month=3), "2020-03-08 00:00"),
    "08/03/2020": (DateTimeObj(year=2020, day=8, month=3), "2020-03-08 00:00"),
    "26 декабря 2023 в 11:00": (DateTimeObj(year=2023, month=12, day=26, hour=11, minute=0, spec=TimeSpecType.PRECISE),
                                "2023-12-26 11:00"),
    "26 декабря 2023 11:00": (DateTimeObj(year=2023, month=12, day=26, hour=11, minute=0, spec=TimeSpecType.PRECISE),
                              "2023-12-26 11:00"),
    "26-12-2023 в 11-00": (DateTimeObj(year=2023, month=12, day=26, hour=11, minute=0, spec=TimeSpecType.PRECISE),
                           "2023-12-26 11:00"),
    "26го числа в час дня": (DateTimeObj(day=26, hour=1, spec=TimeSpecType.PM), "2024-01-26 13:00"),
    "третьего числа в девять утра": (DateTimeObj(day=3, hour=9, spec=TimeSpecType.AM), "2024-01-03 09:00"),
    "в четверг, в девять утра": (DateTimeObj(dow=3, hour=9, spec=TimeSpecType.AM), "2024-01-04 09:00"),
    "в четверг, 28.12.2023, в 10:00": (DateTimeObj(dow=3, day=28, month=12, year=2023,
                                                   hour=10, minute=0, spec=TimeSpecType.PRECISE),
                                       "2023-12-28 10:00"),
    "завтра в десять утра": (DateTimeObj(day_delta=1, hour=10, spec=TimeSpecType.AM), "2023-12-31 10:00"),
    "завтра в полдень": (DateTimeObj(day_delta=1, hour=12, spec=None), "2023-12-31 12:00"),
    "позавчера": (DateTimeObj(day_delta=-2), "2023-12-28 00:00"),
    "вчера": (DateTimeObj(day_delta=-1), "2023-12-29 00:00"),
    "сегодня": (DateTimeObj(day_delta=0), "2023-12-30 00:00"),
    "завтра": (DateTimeObj(day_delta=1), "2023-12-31 00:00"),
    "послезавтра": (DateTimeObj(day_delta=2), "2024-01-01 00:00"),
    "через день": (DateTimeObj(day_delta=2), "2024-01-01 00:00"),  # 1
    "через 2 дня": (DateTimeObj(day_delta=3), "2024-01-02 00:00"),  # 1
    "спустя трое суток": (DateTimeObj(day_delta=4), "2024-01-03 00:00"),  # 1
    "третьего числа": (DateTimeObj(day=3), "2024-01-03 00:00"),
    "третьего в 17-00": (DateTimeObj(day=3, hour=17, minute=0, spec=TimeSpecType.PRECISE), "2024-01-03 17:00"),
    "3 числа": (DateTimeObj(day=3), "2024-01-03 00:00"),
    "3го числа": (DateTimeObj(day=3), "2024-01-03 00:00"),
    "через неделю": (DateTimeObj(day_delta=7), "2024-01-06 00:00"),
    "через 2 недели": (DateTimeObj(day_delta=14), "2024-01-13 00:00"),
    "спустя три недели": (DateTimeObj(day_delta=21), "2024-01-20 00:00"),
    "через месяц": (DateTimeObj(month_delta=1), "2024-01-30 00:00"),
    "через 2 месяца": (DateTimeObj(month_delta=2), "2024-03-01 00:00"),  # не бывает 02-30
    "спустя три месяца": (DateTimeObj(month_delta=3), "2024-03-30 00:00"),
    "через пять минут": (DateTimeObj(minute_delta=5), "2023-12-30 14:05"),
    "через час": (DateTimeObj(hour_delta=1), "2023-12-30 15:00"),
    "через 2 часа": (DateTimeObj(hour_delta=2), "2023-12-30 16:00"),
    "спустя три часа": (DateTimeObj(hour_delta=3), "2023-12-30 17:00"),
    "через два с половиной часа": (DateTimeObj(hour_delta=2, minute_delta=30), "2023-12-30 16:30"),
    "спустя 2 часа 30 минут": (DateTimeObj(hour_delta=2, minute_delta=30), "2023-12-30 16:30"),
    "в час дня": (DateTimeObj(hour=1, spec=TimeSpecType.PM), "2023-12-31 13:00"),  # час дня уже прошел - это на завтра
    "в 2 часа дня": (DateTimeObj(hour=2, spec=TimeSpecType.PM), "2023-12-31 14:00"),  # уже два часа дня - на завтра
    "в два часа ночи": (DateTimeObj(hour=2, spec=TimeSpecType.AM), "2023-12-31 02:00"),  # два часа ночи уже прошли
    "в 8 вечера": (DateTimeObj(hour=8, spec=TimeSpecType.PM), "2023-12-30 20:00"),  # 8 вечера ещё не было - сегодня
    "8 вечера": (DateTimeObj(hour=8, spec=TimeSpecType.PM), "2023-12-30 20:00"),  # 8 вечера ещё не было - сегодня
    "в шесть утра": (DateTimeObj(hour=6, spec=TimeSpecType.AM), "2023-12-31 06:00"),
    "в шесть часов утра": (DateTimeObj(hour=6, spec=TimeSpecType.AM), "2023-12-31 06:00"),
    "в 14 часов": (DateTimeObj(hour=14, spec=None), "2023-12-31 14:00"),  # 14 часов уже было - завтра
    "в 14 часов 30 минут": (DateTimeObj(hour=14, minute=30, spec=None), "2023-12-30 14:30"),
    "в 20 минут": (DateTimeObj(minute=20, spec=None), "2023-12-30 14:20"),
    "в 20 минут шестого": (DateTimeObj(hour=5, minute=20, spec=None), "2023-12-30 17:20"),
    "в половину шестого": (DateTimeObj(hour=5, minute=30, spec=None), "2023-12-30 17:30"),
    "в пол-шестого": (DateTimeObj(hour=5, minute=30, spec=None), "2023-12-30 17:30"),
    "в без пятнадцати шесть": (DateTimeObj(hour=5, minute=45, spec=None), "2023-12-30 17:45"),
    "в без десяти 8": (DateTimeObj(hour=7, minute=50, spec=None), "2023-12-30 19:50"),
    "в без двадцати час": (DateTimeObj(hour=12, minute=40, spec=None), "2023-12-31 12:40"),
    "в без двадцати пяти час": (DateTimeObj(hour=12, minute=35, spec=None), "2023-12-31 12:35"),
    "в без двадцати пяти минут час": (DateTimeObj(hour=12, minute=35, spec=None), "2023-12-31 12:35"),
    "в без двадцати пять часов": (DateTimeObj(hour=4, minute=40, spec=None), "2023-12-30 16:40"),
    "в 14:30": (DateTimeObj(hour=14, minute=30, spec=TimeSpecType.PRECISE), "2023-12-30 14:30"),
    "в 14-30": (DateTimeObj(hour=14, minute=30, spec=TimeSpecType.PRECISE), "2023-12-30 14:30"),
    "в полдень": (DateTimeObj(hour=12, spec=None), "2023-12-31 12:00"),
    "в полночь": (DateTimeObj(hour=0, spec=None), "2023-12-31 00:00"),
    "во вторник": (DateTimeObj(week=None, dow=1), "2024-01-02 00:00"),
    "в пятницу": (DateTimeObj(week=None, dow=4), "2024-01-05 00:00"),
    "в этот вторник": (DateTimeObj(week=0, dow=1), "2023-12-26 00:00"),
    "в эту пятницу": (DateTimeObj(week=0, dow=4), "2023-12-29 00:00"),
    "в прошлый вторник": (DateTimeObj(week=-1, dow=1), "2023-12-19 00:00"),
    "в ту пятницу": (DateTimeObj(week=-1, dow=4), "2023-12-22 00:00"),
    "в следующий вторник": (DateTimeObj(week=1, dow=1), "2024-01-02 00:00"),
    "в следующую пятницу": (DateTimeObj(week=1, dow=4), "2024-01-05 00:00"),
    "2020": (DateTimeObj(year=2020), "2020-12-30 00:00"),
    "2020 года": (DateTimeObj(year=2020), "2020-12-30 00:00"),
    "2020 г.": (DateTimeObj(year=2020), "2020-12-30 00:00"),
    "февраль 2024": (DateTimeObj(year=2024, month=2), "2024-02-28 00:00"),  # 30е число не во всех месяцах, максимум 28е
    "через год": (DateTimeObj(year_delta=1), "2024-12-30 00:00"),
    "через 5 лет": (DateTimeObj(year_delta=5), "2028-12-30 00:00"),
    "спустя три года": (DateTimeObj(year_delta=3), "2026-12-30 00:00"),
    "через год, 2 месяца, 3 дня и 12 часов": (
        DateTimeObj(year_delta=1, month_delta=2, day_delta=4, hour_delta=12),
        "2025-03-06 02:00"
    ),  # 1
}
# [1] Через день = сегодня -> пропускаем день -> целевой день. Так что к указанному в тексте числу дней добавляем 1.
