# logdog

Python package with `logging` utilities

This package is grouped into four main functionalities:

- Encoders <br />
They are the "core" of this package.
They are fully functional, but can still be extended and replaced as needed

- Formatters <br />
They allow you to bring structured logging to your app.
Keys present in log lines (such as `time`, `level` or `message`)
can be easily configured by using a custom format

- Handlers <br />
They are logging handlers.
One of the key features is buffering, so no more 100 emails every minute.
Just one with a summary

- Wrappers <br />
They are just utilities that you can use to simplify the use of logging functions


## Requirements

- Python >= 3.10


## Installation

```bash
pip install -U python-logdog
```
