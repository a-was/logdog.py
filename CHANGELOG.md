# Changelog

# [v0.4.0] - 2024.06.22

[v0.4.0]: https://github.com/a-was/logdog.py/compare/v0.3.3...v0.4.0

- Support duration strings (for example `4h30m28s`)


# [v0.3.3] - 2023.11.18

[v0.3.3]: https://github.com/a-was/logdog.py/compare/v0.3.2...v0.3.3

- Check SMTP connection on `BufferedSmtpHandler` object creation


# [v0.3.2] - 2023.11.04

[v0.3.2]: https://github.com/a-was/logdog.py/compare/v0.3.1...v0.3.2

- Make flushing thread daemonic in `BaseBufferedHandler`


# [v0.3.1] - 2023.10.28

[v0.3.1]: https://github.com/a-was/logdog.py/compare/v0.3.0...v0.3.1

- Fix not clearing buffer after calling `flush()` in `BufferedGoogleChatHandler`
- Add `taskName` key support (Python 3.12+)
- Add checking Python version when using key
- Test code using multiple Python versions


# [v0.3.0] - 2023.10.28

[v0.3.0]: https://github.com/a-was/logdog.py/compare/v0.2.0...v0.3.0

- Create handlers
    - `GoogleChatHandler`
    - `BufferedGoogleChatHandler`
    - `BufferedSmtpHandler`


# [v0.2.0] - 2023.09.18

[v0.2.0]: https://github.com/a-was/logdog.py/compare/v0.1.2...v0.2.0

- Create formatters
    - `LogfmtFormatter`
    - `JsonFormatter`
- Rename Renderer to Encoder
- Code refactor
- Create documentation using `mkdocs`


# [v0.1.2] - 2023.09.09

[v0.1.2]: https://github.com/a-was/logdog.py/compare/v0.1.0...v0.1.2

*Version v0.1.1 was omitted due to a mistake.*

- LogMessageWrapper:
    - Add missing `stacklevel` to log functions
- Update project metadata


# [v0.1.0] - 2023.09.06

[v0.1.0]: https://github.com/a-was/logdog.py/releases/tag/v0.1.0

First release!

Features:

- `LogMessageWrapper`
    - `LogfmtRenderer`
    - `JsonRenderer`
