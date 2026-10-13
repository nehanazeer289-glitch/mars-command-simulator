
from dataclasses import dataclass, field


@dataclass
class RoverState:
    x: int = 0
    y: int = 0
    battery: int = 100
    obstacles: list[tuple[int, int]] = field(default_factory=list)
    current_step: int = 0


@dataclass
class RoverCommand:
    command_id: str
    action: str
    arrival_step: int


@dataclass
class CommandResult:
    command_id: str
    action: str
    status: str
    reason: str
    arrival_step: int
    position_before: tuple[int, int]
    position_after: tuple[int, int]

