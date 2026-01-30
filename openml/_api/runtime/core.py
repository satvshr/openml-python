from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from openml._api.clients import HTTPCache, HTTPClient
from openml._api.config import get_settings
from openml._api.resources import (
    DatasetsV1,
    DatasetsV2,
    FallbackProxy,
    TasksV1,
    TasksV2,
)

if TYPE_CHECKING:
    from openml._api.resources.base import DatasetsAPI, TasksAPI


class APIBackend:
    def __init__(
        self, *, datasets: DatasetsAPI | FallbackProxy, tasks: TasksAPI | FallbackProxy
    ):
        self.datasets = datasets
        self.tasks = tasks


def build_backend(version: str, *, strict: bool) -> APIBackend:
    settings = get_settings()

    # Get config for v1 (lazy init from openml.config)
    v1_config = settings.get_api_config("v1")

    http_cache = HTTPCache(
        path=Path(settings.cache.dir).expanduser(),
        ttl=settings.cache.ttl,
    )

    v1_http_client = HTTPClient(
        server=v1_config.server,
        base_url=v1_config.base_url,
        api_key=v1_config.api_key,
        timeout=v1_config.timeout,
        retries=settings.connection.retries,
        retry_policy=settings.connection.retry_policy,
        cache=http_cache,
    )

    v1 = APIBackend(
        datasets=DatasetsV1(v1_http_client),
        tasks=TasksV1(v1_http_client),
    )

    if version == "v1":
        return v1

    v2 = APIBackend(
        datasets=DatasetsV2(v2_http_client),
        tasks=TasksV2(v2_http_client),
    )

    if strict:
        return v2

    return APIBackend(
        datasets=FallbackProxy(DatasetsV2(v2_http_client), DatasetsV1(v1_http_client)),
        tasks=FallbackProxy(TasksV2(v2_http_client), TasksV1(v1_http_client)),
    )


class APIContext:
    def __init__(self) -> None:
        self._backend = build_backend("v1", strict=False)

    def set_version(self, version: str, *, strict: bool = False) -> None:
        self._backend = build_backend(version=version, strict=strict)

    @property
    def backend(self) -> APIBackend:
        return self._backend
