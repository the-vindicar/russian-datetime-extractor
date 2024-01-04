import typing as tp
from datetime import datetime
import unittest

from date_extracting.extractor import DateTimeExtractor
from date_extracting.binding import bind_reference
from ._samples import ORIGIN, SAMPLES

class TestExtraction(unittest.TestCase):
    """Проверяет корректность извлечения даты и времени,
     а также из привязки к заданной точке отсчёта."""
    extractor: tp.ClassVar[DateTimeExtractor]
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.extractor = DateTimeExtractor()

    @classmethod
    def tearDownClass(cls) -> None:
        del cls.extractor

    def test_examples(self):
        """Каждый пример должен содержать одно и только одно описание даты/времени."""
        for text, (fact, groundtruth) in SAMPLES.items():
            with self.subTest(msg=text):  # позволяет понять, какой элемент списка тестов дал ошибку
                groundtruthvalue = datetime.fromisoformat(groundtruth)
                matches = list(self.extractor(text))
                self.assertEqual(len(matches), 1)
                self.assertEqual(repr(fact), repr(matches[0].fact))  # проверяем извлечение
                value, has_time = bind_reference(matches[0].fact, ORIGIN)
                self.assertEqual(groundtruthvalue, value)  # проверяем привязку
