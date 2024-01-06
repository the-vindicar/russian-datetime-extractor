"""Слова и символы, используемые при разборе даты и времени."""
WORD_BEFORE_YESTERDAY = ['позавчера']
WORD_YESTERDAY = ['вчера']
WORD_TODAY = ['сегодня']
WORD_TOMORROW = ['завтра']
WORD_AFTER_TOMORROW = ['послезавтра']
WORD_YEAR = ['год', 'г', 'лет']
WORD_MONTH = ['месяц']
WORD_WEEK = ['неделя']
WORD_DAY = ['день', 'сутки']
WORD_DAYNUM = ['число']
WORD_HOUR = ['час', 'ч']
PREFIX_HALF = ['пол']
WORD_HALF = ['половина', 'пол']
WORD_SUBTRACTION = ['без']
WORD_HALFHOUR = ['полчаса', 'пол-часа']
WORD_MINUTE = ['минута', 'мин', 'м']
WORD_TIME_DAY = ['день', 'пополудни']
WORD_TIME_MORNING = ['утро']
WORD_TIME_NIGHT = ['ночь']
WORD_TIME_EVENING = ['вечер']
NAMES_MONTH = {
    'январь': 1,
    'янв': 1,
    'февраль': 2,
    'фев': 2,
    'март': 3,
    'мар': 3,
    'апрель': 4,
    'апр': 4,
    'май': 5,
    'июнь': 6,
    'июн': 6,
    'июль': 7,
    'июл': 7,
    'август': 8,
    'авг': 8,
    'сентябрь': 9,
    'сен': 9,
    'октябрь': 10,
    'окт': 10,
    'ноябрь': 11,
    'ноя': 11,
    'декабрь': 12,
    'дек': 12,
}
NAMES_DAYS_OF_WEEK = {
    'понедельник': 0,
    'пн': 0,
    'вторник': 1,
    'вт': 1,
    'среда': 2,
    'ср': 2,
    'четверг': 3,
    'чт': 3,
    'пятница': 4,
    'пт': 4,
    'суббота': 5,
    'сб': 5,
    'воскресенье': 6,
    'вс': 6,
}
WORD_COUNTS = {
    'ноль': 0,
    'один': 1,
    'одни': 1,
    'два': 2,
    'двое': 2,
    'три': 3,
    'трое': 3,
    'четыре': 4,
    'пять': 5,
    'шесть': 6,
    'семь': 7,
    'восемь': 8,
    'девять': 9,
    'десять': 10,
    'одиннадцать': 11,
    'двенадцать': 12,
    'тринадцать': 13,
    'четырнадцать': 14,
    'пятнадцать': 15,
    'шестнадцать': 16,
    'семнадцать': 17,
    'восемнадцать': 18,
    'девятнадцать': 19,
    'двадцать один': 21,
    'двадцать два': 22,
    'двадцать три': 23,
    'двадцать четыре': 24,
    'двадцать пять': 25,
    'двадцать шесть': 26,
    'двадцать семь': 27,
    'двадцать восемь': 28,
    'двадцать девять': 29,
    'двадцать': 20,
    'тридцать': 30,
}
HOUR_WORD_COUNTS = WORD_COUNTS | {'полдень': 12, 'полночь': 0}
WORD_ENUMERATIONS = {
    'нулевой': 0,
    'первый': 1,
    'второй': 2,
    'третий': 3,
    'четвертый': 4,
    'пятый': 5,
    'шестой': 6,
    'седьмой': 7,
    'восьмой': 8,
    'девятый': 9,
    'десятый': 10,
    'одиннадцатый': 11,
    'двенадцатый': 12,
    'тринадцатый': 13,
    'четырнадцатый': 14,
    'пятнадцатый': 15,
    'шестнадцатый': 16,
    'семнадцатый': 17,
    'восемнадцатый': 18,
    'девятнадцатый': 19,
    'двадцатый': 20,
    'двадцать первый': 21,
    'двадцать второй': 22,
    'двадцать третий': 23,
    'двадцать четвертый': 24,
    'двадцать пятый': 25,
    'двадцать шестой': 26,
    'двадцать седьмой': 27,
    'двадцать восьмой': 28,
    'двадцать девятый': 29,
    'тридцатый': 30,
    'тридцать первый': 31,
}
SUFFIX_ENUMERATIONS = ['й', 'е', 'го', 'ому', 'ого']
SEPARATORS_DATE = ['.', '/', '-']
SEPARATORS_TIME = [':', '-']
WORD_AFTER = ['через', 'спустя']
WORD_AGO = ['назад', 'тому назад']
WORD_PREV = ['тот', 'прошлый']
WORD_THIS = ['этот', 'нынешний']
WORD_NEXT = ['следующий', 'следующ', 'след']
WORD_IN = ['в', 'к', 'до']
WORD_JOIN = [',', 'и']