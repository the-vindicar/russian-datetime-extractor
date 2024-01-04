from yargy import (
    rule,
    and_, or_
)
from yargy.pipelines import morph_pipeline
from yargy.predicates import (
    eq, gte, lte, dictionary
)

from .facts import *
from .words import *

__all__ = ['AFTER_SOME_TIME', 'TIME']


HOUR_DELTA_DIGITS = gte(1).interpretation(
    DateTimeFact.hour_delta.custom(int)
)

HOUR_DELTA_WORDS = dictionary(WORD_COUNTS).interpretation(
    DateTimeFact.hour_delta.normalized().custom(WORD_COUNTS.__getitem__)
)

MINUTE_DELTA_DIGITS = gte(1).interpretation(
    DateTimeFact.minute_delta.custom(int)
)

MINUTE_DELTA_WORDS = dictionary(WORD_COUNTS).interpretation(
    DateTimeFact.minute_delta.normalized().custom(WORD_COUNTS.__getitem__)
)

HOUR_COUNT_DIGITS = and_(gte(0), lte(23)).interpretation(
    DateTimeFact.hour.custom(int)
)

HOUR_COUNT_WORDS = dictionary(HOUR_WORD_COUNTS).interpretation(
    DateTimeFact.hour.normalized().custom(HOUR_WORD_COUNTS.__getitem__)
)

HOUR_ENUM_WORDS = dictionary(WORD_ENUMERATIONS).interpretation(
    DateTimeFact.hour.normalized().custom(WORD_ENUMERATIONS.__getitem__)
)

HOUR_START_ENUM_WORDS = dictionary(WORD_ENUMERATIONS).interpretation(
    DateTimeFact.hour.normalized().custom(lambda s: WORD_ENUMERATIONS[s] - 1)
)

HOUR_SUBTRACTED = or_(
    eq('час').interpretation(
        DateTimeFact.hour.const(12)
    ),
    and_(gte(0), lte(23)).interpretation(
        DateTimeFact.hour.custom(lambda s: int(s) - 1)
    ),
    dictionary(HOUR_WORD_COUNTS).interpretation(
        DateTimeFact.hour.normalized().custom(lambda s: HOUR_WORD_COUNTS[s] - 1)
    ),
)

MINUTE_SUBTRACTED = morph_pipeline(WORD_COUNTS.keys()).interpretation(
    DateTimeFact.minute.normalized().custom(lambda s: 60 - WORD_COUNTS[s])
)

MINUTE_COUNT_DIGITS = and_(gte(0), lte(59)).interpretation(
    DateTimeFact.minute.custom(int)
)

MINUTE_COUNT_WORDS = morph_pipeline(WORD_COUNTS.keys()).interpretation(
    DateTimeFact.minute.normalized().custom(WORD_COUNTS.__getitem__)
)

AFTER_SOME_TIME = rule(
    or_(
        rule(  # "через X часов", где X словом или числом = прибавить к текущему времени X часов
            or_(HOUR_DELTA_DIGITS, HOUR_DELTA_WORDS),
            morph_pipeline(WORD_HOUR),  # "часов"
        ),
        rule(  # "через X с половиной часов", где X словом или числом = прибавить к текущему времени X часов 30 минут
            or_(HOUR_DELTA_DIGITS, HOUR_DELTA_WORDS),
            eq('с'),
            morph_pipeline(WORD_HALF).interpretation(
                DateTimeFact.minute_delta.const(30)
            ),  # "с половиной"
            morph_pipeline(WORD_HOUR),  # "часов"
        ),
        # просто "через час"
        morph_pipeline(WORD_HOUR).interpretation(
            DateTimeFact.hour_delta.const(1)  # через час = +1 час к дате
        ),
        # "через полчаса"
        or_(
            rule(
                morph_pipeline(PREFIX_HALF),
                morph_pipeline(WORD_HOUR)
            ),
            morph_pipeline(WORD_HALFHOUR),
        ).interpretation(
            DateTimeFact.minute_delta.const(30)  # через полчаса = +30 минут к дате
        ),
    ).optional(),
    or_(
        rule(  # "через X минут", где X словом или числом = прибавить к текущему времени X минут
            or_(MINUTE_DELTA_DIGITS, MINUTE_DELTA_WORDS),
            morph_pipeline(WORD_MINUTE),  # "минут"
        ),
        # просто "через минуту"
        morph_pipeline(WORD_MINUTE).interpretation(
            DateTimeFact.minute_delta.const(1)  # через минуту = +1 минута к дате
        )
    ).optional(),
)

HOUR_COUNT = or_(HOUR_COUNT_DIGITS, HOUR_COUNT_WORDS)
MINUTE_COUNT = or_(MINUTE_COUNT_DIGITS, MINUTE_COUNT_WORDS)
TIME_SPEC = or_(
    rule(
        HOUR_COUNT_DIGITS,
        or_(*[eq(s) for s in SEPARATORS_TIME]).interpretation(
            DateTimeFact.spec.const(TimeSpecType.PRECISE)
        ),
        MINUTE_COUNT_DIGITS
    ),
    rule(
        HOUR_COUNT,
        morph_pipeline(WORD_HOUR).optional(),
        rule(
            MINUTE_COUNT,
            morph_pipeline(WORD_MINUTE)
        ).optional(),
    ),
    rule(
        morph_pipeline(WORD_SUBTRACTION),
        MINUTE_SUBTRACTED,
        morph_pipeline(WORD_MINUTE).optional(),
        HOUR_SUBTRACTED,
    ),
    rule(
        or_(
            rule(MINUTE_COUNT, morph_pipeline(WORD_MINUTE)),
            rule(
                morph_pipeline(WORD_HALF).interpretation(
                    DateTimeFact.minute.const(30)
                ),
                eq('-').optional(),
            ),
        ),
        HOUR_START_ENUM_WORDS.optional()
    ),
)

AM = morph_pipeline(WORD_TIME_MORNING + WORD_TIME_NIGHT).interpretation(
    DateTimeFact.spec.const(TimeSpecType.AM)
)
PM = morph_pipeline(WORD_TIME_DAY + WORD_TIME_EVENING).interpretation(
    DateTimeFact.spec.const(TimeSpecType.PM)
)

TIME = rule(
    or_(
        rule(
            morph_pipeline(WORD_HOUR).interpretation(
                DateTimeFact.hour.const(1)
            ),
            or_(AM, PM),
        ),
        rule(
            HOUR_COUNT,
            morph_pipeline(WORD_HOUR).optional(),
            or_(AM, PM),
        ),
        TIME_SPEC
    ),
)
