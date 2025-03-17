from typing import Any, Awaitable, Callable, Dict, List, TypeAlias

TData: TypeAlias = Dict[str, Any]
TLoc: TypeAlias = List[str | int]

SendWs = Callable[[str], Awaitable[None]]
