import typing as tp
import dataclasses
from datetime import datetime
from .extractor import DateTimeExtractor
from .binding import bind_reference, BindType

__all__ = ['DateTime']


_DT = tp.TypeVar('_DT', bound='DateTime')


@dataclasses.dataclass(frozen=True)
class DateTime:
    """
    Contains date and, optionally, time reference extracted from a natural russian text.
    Also points to the substring from which the data has been extracted.

    Attributes:

    - datetime  : datetime - extracted date/datetime
    - has_time  : bool     - if True, `datetime` contains a time portion
    - idx_start : int      - starting position of the reference in the text
    - idx_end   : int      - ending position of the reference in the text
    - text      : str      - substring containing the reference
    """
    datetime: datetime
    has_time: bool
    idx_start: int
    idx_end: int
    text: str

    _extractor: tp.ClassVar[DateTimeExtractor] = DateTimeExtractor()

    @classmethod
    def extract(cls: tp.Type[_DT], text: str, direction: BindType, origin: datetime) -> tp.List[_DT]:
        """
        Извлекает из предложенного текста все отсылки к дате и времени.
        Отсылки привязываются к указанной точке отсчёта, используя указанное предпочтительное направление во времени.
        * BindType.FUTURE - поиск ведётся в будущее, если только явно не указана дата в прошлом.
        * BindType.PAST - поиск ведётся в прошлое, если только явно не указана дата в будущем.
        * BindType.CLOSEST - поиск ведётся в обе стороны, возвращается ближайшее из двух значений.
        При равной дистанции возвращается дата в будущем.

        :param text: Текст, из которого извлекаются упоминания даты и времени.
        :param direction: Направление, в котором ведётся поиск подходящей даты для неоднозначного упоминания.
        :param origin: точка отсчёта, относительно которой вычисляется дата.
        :return: Список найденных дат, с указанием на наличие времени и подстроку, которая их содержит.
        """
        results = []
        for match in cls._extractor(text):
            substr = text[match.start:match.stop]
            dt, has_time = bind_reference(match.fact, direction, origin)
            results.append(cls(
                datetime=dt,
                has_time=has_time,
                idx_start=match.start,
                idx_end=match.stop,
                text=substr))
        return results
