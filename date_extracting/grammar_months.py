from yargy import (
    rule,
    and_, or_
)
from yargy.pipelines import morph_pipeline
from yargy.predicates import (
    gte, lte, dictionary, )

from .facts import *
from .words import *

__all__ = ['AFTER_SOME_MONTHS', 'SOME_MONTHS_AGO',
           'MONTH_NAME', 'MONTH_NUMBER', 'MONTH']

# *три* месяца
MONTH_COUNT_WORDS = morph_pipeline(WORD_COUNTS).interpretation(
    DateTimeFact.month_delta.normalized().custom(WORD_COUNTS.__getitem__)
)
# *3* месяца
MONTH_COUNT_DIGITS = gte(1).interpretation(
    DateTimeFact.month_delta.custom(int)
)

# *три* месяца назад
MONTH_COUNT_WORDS_NEG = morph_pipeline(WORD_COUNTS).interpretation(
    DateTimeFact.month_delta.normalized().custom(lambda s: -WORD_COUNTS[s])
)
# *3* месяца назад
MONTH_COUNT_DIGITS_NEG = gte(1).interpretation(
    DateTimeFact.month_delta.custom(lambda s: -int(s))
)

MONTH_NAME = dictionary(NAMES_MONTH).interpretation(
    DateTimeFact.month.normalized().custom(NAMES_MONTH.__getitem__)
)

MONTH_NUMBER = and_(
    gte(1),
    lte(12)
).interpretation(
    DateTimeFact.month.custom(int)
)

MONTH = or_(
    MONTH_NAME,
    rule(
        morph_pipeline(WORD_PREV).interpretation(
            DateTimeFact.month_delta.const(-1)
        ),
        morph_pipeline(WORD_MONTH)
    ),
    rule(
        morph_pipeline(WORD_NEXT).interpretation(
            DateTimeFact.month_delta.const(1)
        ),
        morph_pipeline(WORD_MONTH)
    ),
)

AFTER_SOME_MONTHS = rule(
    or_(
        rule(  # "через X месяцев", где X словом или числом = прибавить к текущей дате X
            or_(MONTH_COUNT_DIGITS, MONTH_COUNT_WORDS).interpretation(
                DateTimeFact.month_delta
            ),
            morph_pipeline(WORD_MONTH),  # "месяцев"
        ),
        # просто "через месяц"
        morph_pipeline(WORD_MONTH).interpretation(
            DateTimeFact.month_delta.const(1)  # через месяц = +1 месяц к дате
        )
    )
)

SOME_MONTHS_AGO = rule(
    or_(
        rule(  # "X месяцев назад", где X словом или числом = вычесть из текущей даты X
            or_(MONTH_COUNT_DIGITS_NEG, MONTH_COUNT_WORDS_NEG),
            morph_pipeline(WORD_MONTH),  # "месяцев"
        ),
        # просто "месяц назад"
        morph_pipeline(WORD_MONTH).interpretation(
            DateTimeFact.month_delta.const(-1)  # месяц назад = -1 месяц к дате
        )
    )
)
