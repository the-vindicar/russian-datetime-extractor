import locale
from datetime import datetime
from date_extracting import DateTime

texts = [
    "Мероприятие начнётся 21 декабря 2023, в 12 часов 00 минут.",
    "21 декабря 2023, в 12:30 будет собрание.",
    "21 декабря 2023 к 12:30 нужно будет зайти в дирекцию.",
    "21 декабря в полдень состоится заседание учёного совета.",
    "В эту пятницу в 10 часов начнётся экзамен.",
    "В следующую пятницу в 12 часов будет собрание.",
    "Собрание состоится послезавтра, в 12 часов.",
    "Послезавтра будет собрание",
    "21 числа будет корпоратив.",
    "Приходите на чаепитие сегодня в 12 часов!",
    "Через 3 дня в 18:00 тренировка",
    "Футбол начнётся через два часа.",
]

locale.setlocale(0, 'RU-ru')
now = datetime.now()

for text in texts:
    results = DateTime.extract(text, now)
    print('[+]' if len(results) == 1 else '[-]', text)
    for r in results:
        dt = r.datetime.strftime('%A, %d %B %Y, %H:%M' if r.has_time else '%A, %d %B %Y')
        print(f'    {r.text} -> {dt}')
