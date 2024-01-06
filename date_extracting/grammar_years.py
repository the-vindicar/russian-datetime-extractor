from yargy import (
    rule,
    and_, or_
)
from yargy.pipelines import morph_pipeline
from yargy.predicates import (
    eq, gte, lte, length_eq,
)

from .facts import *
from .words import *

__all__ = ['AFTER_SOME_YEARS', 'SOME_YEARS_AGO',
           'YEAR_NUMBER', 'YEAR_NUMBER_LONG']

# *три* года
YEAR_COUNT_WORDS = morph_pipeline(WORD_COUNTS).interpretation(
    DateTimeFact.year_delta.normalized().custom(WORD_COUNTS.__getitem__)
)
# *3* года
YEAR_COUNT_DIGITS = gte(1).interpretation(
    DateTimeFact.year_delta.custom(int)
)
# *три* года назад
YEAR_COUNT_WORDS_NEG = morph_pipeline(WORD_COUNTS).interpretation(
    DateTimeFact.year_delta.normalized().custom(lambda s: -WORD_COUNTS[s])
)
# *3* года назад
YEAR_COUNT_DIGITS_NEG = gte(1).interpretation(
    DateTimeFact.year_delta.custom(lambda s: -int(s))
)
# *2020* год
YEAR_NUMBER_LONG = rule(
    and_(gte(1900), lte(2100)).interpretation(
        DateTimeFact.year.custom(int)
    ),
    or_(*[eq(suffix) for suffix in SUFFIX_ENUMERATIONS]).optional()
)


# *20й* год
def short_year(s: str) -> int:
    y = int(s)
    return y + 2000


YEAR_NUMBER_SHORT = rule(
    and_(length_eq(2), gte(0), lte(99)).interpretation(
        DateTimeFact.year.custom(short_year)
    ),
    or_(*[eq(suffix) for suffix in SUFFIX_ENUMERATIONS]).optional()
)

AFTER_SOME_YEARS = rule(
    or_(
        rule(  # "через X лет", где X словом или числом = прибавить к текущей дате X лет
            or_(YEAR_COUNT_DIGITS, YEAR_COUNT_WORDS),
            morph_pipeline(WORD_YEAR),  # "год"
        ),
        # просто "через год"
        morph_pipeline(WORD_YEAR).interpretation(
            DateTimeFact.year_delta.const(1)  # через год = +1 год к дате
        )
    )
)

SOME_YEARS_AGO = rule(
    or_(
        rule(  # "X лет назад", где X словом или числом = вычесть из текущей даты X лет
            or_(YEAR_COUNT_DIGITS_NEG, YEAR_COUNT_WORDS_NEG),
            morph_pipeline(WORD_YEAR),  # "год"
        ),
        # просто "год назад"
        morph_pipeline(WORD_YEAR).interpretation(
            DateTimeFact.year_delta.const(-1)  # год назад = -1 год к дате
        )
    )
)

YEAR_NUMBER = rule(
    or_(YEAR_NUMBER_LONG, YEAR_NUMBER_SHORT),
    or_(*[eq(suffix) for suffix in SUFFIX_ENUMERATIONS]).optional(),
    morph_pipeline(WORD_YEAR).optional()
)
