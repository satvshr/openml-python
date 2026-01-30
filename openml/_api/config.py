from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class RetryPolicy(str, Enum):
    HUMAN = "human"
    ROBOT = "robot"


@dataclass
class APIConfig:
    server: str
    base_url: str
    api_key: str
    timeout: int = 10  # seconds


@dataclass
class ConnectionConfig:
    retries: int = 3
    retry_policy: RetryPolicy = RetryPolicy.HUMAN


@dataclass
class CacheConfig:
    dir: str = "~/.openml/cache"
    ttl: int = 60 * 60 * 24 * 7  # one week


class Settings:
    def __init__(self) -> None:
        self.api_configs: dict[str, APIConfig] = {}
        self.connection = ConnectionConfig()
        self.cache = CacheConfig()
        self._initialized = False

    def get_api_config(self, version: str) -> APIConfig:
        """Get API config for a version, with lazy initialization from openml.config."""
        if not self._initialized:
            self._init_from_legacy_config()
        if version not in self.api_configs:
            raise NotImplementedError(
                f"API {version} is not yet available. "
                f"Supported versions: {list(self.api_configs.keys())}"
            )
        return self.api_configs[version]

    def _init_from_legacy_config(self) -> None:
        """Lazy init from openml.config to avoid circular imports."""
        if self._initialized:
            return

        # Import here to avoid circular import at module load time
        import openml.config as legacy

        # Parse server URL to extract base components
        # e.g., "https://www.openml.org/api/v1/xml" -> server="https://www.openml.org/"
        server_url = legacy.server
        if "/api" in server_url:
            server_base = server_url.rsplit("/api", 1)[0] + "/"
        else:
            server_base = server_url

        self.api_configs["v1"] = APIConfig(
            server=server_base,
            base_url="api/v1/xml/",
            api_key=legacy.apikey,
        )

        # Sync connection settings from legacy config
        self.connection = ConnectionConfig(
            retries=legacy.connection_n_retries,
            retry_policy=RetryPolicy(legacy.retry_policy),
        )

        # Sync cache settings from legacy config
        self.cache = CacheConfig(
            dir=str(legacy._root_cache_directory),
        )

        self._initialized = True


settings = Settings(
    api=APISettings(
        v1=APIConfig(
            server="https://www.openml.org/",
            base_url="api/v1/xml/",
            api_key="...",
        ),
        v2=APIConfig(
            server="http://127.0.0.1:8001/",
            base_url="",
            api_key="...",
        ),
    ),
    connection=ConnectionConfig(),
    cache=CacheConfig(),
)


_settings = None


def get_settings() -> Settings:
    """Get settings singleton, creating on first access.

    Settings are lazily initialized from openml.config when first accessed,
    avoiding circular imports at module load time.
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
