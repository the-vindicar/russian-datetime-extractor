Инструмент предназначен для извлечения упоминаний даты/времени из текста на естественном русском языке,
с последующей привязкой к указанному моменту времени.
Это позволяет обрабатывать неформальные и неточные описания вроде 
"послезавтра", "следующий вторник", "через час" или "без двадцати четыре".

Основан на [natasha/yargy](https://github.com/natasha/yargy). 
Дополнительные примеры текста можно найти в файле `tests/_samples.py`.

-----

This tool allows extraction of date/time references from the given Russian text. 
Extracted references are bound to the given origin point, with the general idea of planning a future event.
As such, the tool tends to pick the closest matching date/time *in the future*,
unless a past date is explicitly and fully specified.
This allows the tool to process Russian equivalents of "the day after tomorrow",
"next tuesday", "in an hour" or "twenty minutes to four".

Based on [natasha/yargy](https://github.com/natasha/yargy). 
Extra text samples can be found in `tests/_samples.py`.