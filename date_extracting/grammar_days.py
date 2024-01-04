from yargy import (
    rule,
    and_, or_
)
from yargy.pipelines import morph_pipeline
from yargy.predicates import (
    eq, gte, lte, dictionary, )

from .facts import *
from .words import *

__all__ = ['AFTER_SOME_DAYS', 'DAY_NUMBER', 'SPECIAL_DAY_NAMES']

# *три* дня
DAY_COUNT_WORDS = dictionary(WORD_COUNTS).interpretation(
    DateTimeFact.day_delta.normalized().custom(WORD_COUNTS.__getitem__)
)
# *3* дня
DAY_COUNT_DIGITS = gte(1).interpretation(
    DateTimeFact.day_delta.custom(int)
)
# *третье* число
DAY_NUMBER_WORDS = dictionary(WORD_ENUMERATIONS).interpretation(
    DateTimeFact.day.normalized().custom(WORD_ENUMERATIONS.__getitem__)
)
# *3* число
DAY_NUMBER_DIGITS = rule(
    and_(gte(1), lte(31)).interpretation(
        DateTimeFact.day.custom(int)
    ),
    or_(*[eq(suffix) for suffix in SUFFIX_ENUMERATIONS]).optional()
)

SPECIAL_DAY_NAMES = or_(
    rule(morph_pipeline(WORD_BEFORE_YESTERDAY)).interpretation(DateTimeFact.day_delta.const(-2)),
    rule(morph_pipeline(WORD_YESTERDAY)).interpretation(DateTimeFact.day_delta.const(-1)),
    rule(morph_pipeline(WORD_TODAY)).interpretation(DateTimeFact.day_delta.const(0)),
    rule(morph_pipeline(WORD_TOMORROW)).interpretation(DateTimeFact.day_delta.const(1)),
    rule(morph_pipeline(WORD_AFTER_TOMORROW)).interpretation(DateTimeFact.day_delta.const(2)),
)

AFTER_SOME_DAYS = rule(
        or_(
            rule(  # "через X дней", где X словом или числом = прибавить к текущей дате X+1
                or_(DAY_COUNT_DIGITS, DAY_COUNT_WORDS).interpretation(
                    DateTimeFact.day_delta.custom(lambda i: int(i) + 1)
                ),
                morph_pipeline(WORD_DAY),  # "дней"
            ),
            # просто "через день"
            morph_pipeline(WORD_DAY).interpretation(
                DateTimeFact.day_delta.const(2)  # через день = послезавтра = +2 дня к дате
            )
        )
    )

DAY_NUMBER = or_(DAY_NUMBER_WORDS, DAY_NUMBER_DIGITS)
