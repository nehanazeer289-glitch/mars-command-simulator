from backend.engine import RoverEngine
from backend.models import RoverState


def test_command_waits_for_arrival():
    engine = RoverEngine()
    command = engine.send_command("MOVE_FORWARD", delay_steps=2)

    assert engine.process_command(command) is None

    engine.advance_time(2)
    result = engine.process_command(command)

    assert result.status == "ACCEPTED"


def test_command_rejected_if_obstacle_appears():
    rover = RoverState()
    engine = RoverEngine(rover)

    command = engine.send_command("MOVE_FORWARD", delay_steps=2)

    # An obstacle appears while the command is travelling.
    rover.obstacles.append((1, 0))

    engine.advance_time(2)
    result = engine.process_command(command)

    assert result.status == "REJECTED"
    assert rover.x == 0