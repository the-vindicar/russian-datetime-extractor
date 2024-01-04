from yargy import (
    rule,
    or_
)
from yargy.pipelines import morph_pipeline
from yargy.predicates import (
    dictionary, )

from .facts import *
from .words import *

__all__ = ['WEEKDAY']

WEEKDAY = rule(
    morph_pipeline(WORD_IN).optional(),
    or_(
        morph_pipeline(WORD_PREV).interpretation(
            DateTimeFact.week.const(-1),
        ),
        morph_pipeline(WORD_THIS).interpretation(
            DateTimeFact.week.const(0)
        ),
        morph_pipeline(WORD_NEXT).interpretation(
            DateTimeFact.week.const(1)
        ),
    ).optional(),
    dictionary(NAMES_DAYS_OF_WEEK).interpretation(
        DateTimeFact.dow.normalized().custom(NAMES_DAYS_OF_WEEK.__getitem__)
    )
)

