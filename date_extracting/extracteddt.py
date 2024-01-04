import typing as tp
import dataclasses
from datetime import datetime
from .extractor import DateTimeExtractor
from .binding import bind_reference

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
    def extract(cls: tp.Type[_DT], text: str, origin: datetime) -> tp.List[_DT]:
        results = []
        for match in cls._extractor(text):
            substr = text[match.start:match.stop]
            dt, has_time = bind_reference(match.fact, origin)
            results.append(cls(
                datetime=dt,
                has_time=has_time,
                idx_start=match.start,
                idx_end=match.stop,
                text=substr))
        return results
