from typing import Any, Callable
from dataclasses import dataclass


@dataclass
class CryptioTable:
    table: str
    endpoint: str
    transform_fn: Callable[[Any], Any]
    schema: Any
