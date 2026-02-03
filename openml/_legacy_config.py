from __future__ import annotations

from typing import Any


class LegacyConfigMeta(type):
    def __getattr__(cls, name: str) -> Any:
        import openml

        return getattr(openml._config, name)

    def __setattr__(cls, name: str, value: Any) -> None:
        import openml

        setattr(openml._config, name, value)


class LegacyConfig(metaclass=LegacyConfigMeta):
    pass
