from enum import Enum
from dataclasses import dataclass, field

class CheckStatus(Enum):
    PASS = 3
    WARNING = 2
    FAIL = 1
    NA = -1

@dataclass
class SidCheckDetails:
    sid: str
    notes: list[int] = field(default_factory=list)

@dataclass
class SrdCheckDetails:
    routes: list[int]
    entry_point: str | None = None
    exit_point: str | None = None
    verified_route: int | None = None

@dataclass
class FlCheckDetails:
    min_fl: int
    max_fl: int

@dataclass
class CheckResult:
    status: CheckStatus
    reason: str | None = None
    details: SidCheckDetails | SrdCheckDetails | FlCheckDetails | None = None

@dataclass
class Aircraft:
    callsign: str
    route: str
    fl: int

    aircraft_type: str
    aircraft_name: str | None
    wake_cat: str
    wake_cat_dep_caa: str | None
    wake_cat_arr_caa: str | None

    dep: str
    arr: str
    dep_name: str
    arr_name: str

    checks: dict[str, CheckResult]


