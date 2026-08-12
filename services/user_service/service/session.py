from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Callable, Generator


@dataclass
class SessionMixin:
    _session_provider: Callable[[], Any] | None = field(
        default=None, init=False, repr=False
    )

    @contextmanager
    def get_session(self) -> Generator[Any, Any, None]:
        if self._session_provider is None:
            raise NotImplementedError("_session_provider must be set on the instance")
        cm = self._session_provider()
        with cm as ctx:
            yield ctx
