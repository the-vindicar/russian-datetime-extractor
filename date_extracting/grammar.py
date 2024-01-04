from yargy import (
    rule,
    or_
)
from yargy.pipelines import morph_pipeline
from yargy.predicates import (
    eq, )

from .facts import DateTimeFact
from .grammar_days import AFTER_SOME_DAYS, DAY_NUMBER, SPECIAL_DAY_NAMES
from .grammar_months import AFTER_SOME_MONTHS, MONTH_NAME, MONTH_NUMBER
from .grammar_time import AFTER_SOME_TIME, TIME
from .grammar_weekdays import WEEKDAY
from .grammar_weeks import AFTER_SOME_WEEKS
from .grammar_years import AFTER_SOME_YEARS, YEAR_NUMBER, YEAR_NUMBER_LONG
from .words import *

INTERVAL_JOIN = or_(*[eq(w) for w in WORD_JOIN])

AFTER_TIME_INTERVAL = rule(
    morph_pipeline(WORD_AFTER),
    AFTER_SOME_YEARS.optional(),
    INTERVAL_JOIN.optional(),
    AFTER_SOME_MONTHS.optional(),
    INTERVAL_JOIN.optional(),
    AFTER_SOME_DAYS.optional(),
    INTERVAL_JOIN.optional(),
    AFTER_SOME_TIME,
)

AFTER_INTERVAL = rule(
    morph_pipeline(WORD_AFTER),
    or_(
        AFTER_SOME_WEEKS,
        rule(
            AFTER_SOME_YEARS.optional(),
            INTERVAL_JOIN.optional(),
            AFTER_SOME_MONTHS.optional(),
            INTERVAL_JOIN.optional(),
            AFTER_SOME_DAYS,
        ),
        rule(
            AFTER_SOME_YEARS.optional(),
            INTERVAL_JOIN.optional(),
            AFTER_SOME_MONTHS,
        ),
        AFTER_SOME_YEARS,
    ),
)
# прямые варианты задания даты
DATE_SPEC = or_(
    or_(  # задание даты числами
        *[rule(  # день-месяц-год
            DAY_NUMBER,
            eq(sep),
            MONTH_NUMBER,
            eq(sep),
            YEAR_NUMBER,
        ) for sep in SEPARATORS_DATE],
        *[rule(  # день-месяц
            DAY_NUMBER,
            eq(sep),
            MONTH_NUMBER,
        ) for sep in SEPARATORS_DATE],
        *[rule(  # год-месяц-день
            YEAR_NUMBER_LONG,
            eq(sep),
            MONTH_NUMBER,
            eq(sep),
            DAY_NUMBER,
        ) for sep in SEPARATORS_DATE],
    ),
    rule(  # 14 мартобря 2020 или просто 14 мартобря
        DAY_NUMBER,
        MONTH_NAME,
        YEAR_NUMBER.optional(),
    ),
    rule(  # 14 числа
        DAY_NUMBER,
        morph_pipeline(WORD_DAYNUM).optional()
    ),
    rule(  # январь
        MONTH_NAME,
        YEAR_NUMBER.optional(),
    ),
    YEAR_NUMBER,  # 2020
)
# обобщённые варианты задания даты
DATE = or_(
    AFTER_INTERVAL,  # через N дней и т.п.
    SPECIAL_DAY_NAMES,  # сегодня, завтра и т.п.
    rule(WEEKDAY, eq(',').optional(), DATE_SPEC),  # четверг, четвёртого числа
    rule(  # четвёртого числа, в четверг
        DATE_SPEC,
        eq(',').optional(), or_(*[eq(w) for w in WORD_IN]).optional(),
        WEEKDAY
    ),
    WEEKDAY,  # четверг
    DATE_SPEC  # прямые варианты задания даты
)
# обобщённая грамматика задания даты и времени
DATETIME = or_(
    AFTER_TIME_INTERVAL,  # через три часа
    TIME,  # в три часа
    rule(  # четвёртого января, в три часа
        DATE,
        eq(',').optional(),
        or_(*[eq(w) for w in WORD_IN]).optional(),
        TIME
    ),
    DATE  # четвёртого января
).interpretation(
    DateTimeFact
)
