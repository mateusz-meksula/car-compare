from enum import Enum


APP_WELCOME_MESSAGE = """
┌───────────────────────────────────────────────────────────────────────────────┐
│    _|_|_|                                                                     │
│  _|          _|_|_|  _|  _|_|                                                 │
│  _|        _|    _|  _|_|                                                     │
│  _|        _|    _|  _|                                                       │
│    _|_|_|    _|_|_|  _|                                                       │
│    _|_|_|                                                                     │
│  _|          _|_|    _|_|_|  _|_|    _|_|_|      _|_|_|  _|  _|_|    _|_|     │
│  _|        _|    _|  _|    _|    _|  _|    _|  _|    _|  _|_|      _|_|_|_|   │
│  _|        _|    _|  _|    _|    _|  _|    _|  _|    _|  _|        _|         │
│    _|_|_|    _|_|    _|    _|    _|  _|_|_|      _|_|_|  _|          _|_|_|   │
│                                      _|                                       │
│                                      _|                                       │
└───────────────────────────────────────────────────────────────────────────────┘

Created by Mati
"""  # noqa: E501


class SupportedSites(Enum):
    OTOMOTO = "otomoto"

    def __str__(self) -> str:
        return self.value
