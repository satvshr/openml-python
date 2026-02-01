from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from openml._api.clients import HTTPCache, HTTPClient
from openml._api.config import Settings
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
    def __init__(self, *, datasets: DatasetsAPI | FallbackProxy, tasks: TasksAPI | FallbackProxy):
        self.datasets = datasets
        self.tasks = tasks


def build_backend(version: str, *, strict: bool) -> APIBackend:
    settings = Settings.get()

    # Get config for v1. On first access, this triggers lazy initialization
    # from openml.config, reading the user's actual API key, server URL,
    # cache directory, and retry settings. This avoids circular imports
    # (openml.config is imported inside the method, not at module load time)
    # and ensures we use the user's configured values rather than hardcoded defaults.
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

    # V2 support. Currently v2 is not yet available,
    # so get_api_config("v2") raises NotImplementedError. When v2 becomes available,
    # its config will be added to Settings._init_from_legacy_config().
    # In strict mode: propagate the error.
    # In non-strict mode: silently fall back to v1 only.
    try:
        v2_config = settings.get_api_config("v2")
    except NotImplementedError:
        if strict:
            raise
        # Non-strict mode: fall back to v1 only
        return v1

    v2_http_client = HTTPClient(
        server=v2_config.server,
        base_url=v2_config.base_url,
        api_key=v2_config.api_key,
        timeout=v2_config.timeout,
        retries=settings.connection.retries,
        retry_policy=settings.connection.retry_policy,
        cache=http_cache,
    )

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
