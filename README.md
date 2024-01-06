Инструмент предназначен для извлечения упоминаний даты/времени из текста на естественном русском языке,
с последующей привязкой к указанному моменту времени.
Это позволяет обрабатывать неформальные и неточные описания вроде 
"послезавтра", "следующий вторник", "через час" или "без двадцати четыре".
При этом есть возможность указать предпочтительное направление поиска даты - например,
искать "5е число" в будущем, в прошлом или выбрать ближайшее из двух.

Основан на [natasha/yargy](https://github.com/natasha/yargy). 
Дополнительные примеры текста можно найти в файле `tests/_samples.py`.

-----

This tool allows extraction of date/time references from the given Russian text. 
Extracted references are bound to the given origin point, with the ability to set the search direction.
This allows the tool to process Russian equivalents of "the day after tomorrow",
"next tuesday", "in an hour" or "twenty minutes to four".
Thanks to direction context, the tool can look for "5th day" in the future, in the past, or pick the closest of the two.

Based on [natasha/yargy](https://github.com/natasha/yargy). 
Extra text samples can be found in `tests/_samples.py`.