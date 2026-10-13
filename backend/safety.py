
from backend.models import RoverState, RoverCommand


def check_command(
    rover: RoverState,
    command: RoverCommand,
) -> tuple[bool, str]:

    if command.action == "MOVE_FORWARD":
        next_position = (rover.x + 1, rover.y)

        if next_position in rover.obstacles:
            return False, "Obstacle detected at the next position."

        if rover.battery < 5:
            return False, "Insufficient battery to move safely."

        return True, "Path is clear and battery is sufficient."

    elif command.action == "TAKE_PHOTO":
        if rover.battery < 2:
            return False, "Insufficient battery to take a photo."

        return True, "Battery is sufficient to take a photo."

    return False, f"Unknown command: {command.action}"
