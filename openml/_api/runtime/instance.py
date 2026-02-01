from __future__ import annotations

from openml._api.runtime.core import APIBackend, build_backend

_backend: APIBackend = build_backend("v1", strict=False)
