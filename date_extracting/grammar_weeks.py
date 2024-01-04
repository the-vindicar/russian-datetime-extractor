from yargy import (
    rule,
    or_
)
from yargy.pipelines import morph_pipeline
from yargy.predicates import (
    gte, dictionary, )

from .facts import *
from .words import *

__all__ = ['AFTER_SOME_WEEKS']

WEEK_COUNT_DIGITS = gte(1).interpretation(
    DateTimeFact.day_delta.custom(lambda s: 7 * int(s))
)

WEEK_COUNT_WORDS = dictionary(WORD_COUNTS).interpretation(
    DateTimeFact.day_delta.normalized().custom(lambda s: 7 * WORD_COUNTS[s])
)

AFTER_SOME_WEEKS = rule(
    or_(
        rule(  # "через X недель", где X словом или числом = прибавить к текущей дате X недель
            or_(WEEK_COUNT_DIGITS, WEEK_COUNT_WORDS),
            morph_pipeline(WORD_WEEK),  # "недель"
        ),
        # просто "через неделю"
        morph_pipeline(WORD_WEEK).interpretation(
            DateTimeFact.day_delta.const(7)  # через неделю = +7 дней к дате
        )
    )
)

