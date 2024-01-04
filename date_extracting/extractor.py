"""Использует механизмы библиотеки Natasha для извлечения фактов из фрагментов текста,
подходящих по виду под указанную грамматику."""
from natasha import MorphVocab
from natasha.extractors import Extractor
from .grammar import DATETIME


class DateTimeExtractor(Extractor):
    """Извлекает из текста описания даты и времени."""
    def __init__(self, morph=None):
        if morph is None:
            morph = MorphVocab()
        Extractor.__init__(self, DATETIME, morph)
