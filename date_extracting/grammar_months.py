from yargy import (
    rule,
    and_, or_
)
from yargy.pipelines import morph_pipeline
from yargy.predicates import (
    gte, lte, dictionary, )

from .facts import *
from .words import *

__all__ = ['AFTER_SOME_MONTHS', 'MONTH_NAME', 'MONTH_NUMBER']

# *три* месяца
MONTH_COUNT_WORDS = dictionary(WORD_COUNTS).interpretation(
    DateTimeFact.month_delta.normalized().custom(WORD_COUNTS.__getitem__)
)
# *3* месяца
MONTH_COUNT_DIGITS = gte(1).interpretation(
    DateTimeFact.month_delta.custom(int)
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
