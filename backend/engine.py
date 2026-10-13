
from backend.models import RoverState, RoverCommand, CommandResult
from backend.safety import check_command


class RoverEngine:
    def __init__(self, rover=None):
        self.rover = rover or RoverState()

    def send_command(self, action, delay_steps=2):
        command = RoverCommand(
            command_id=f"CMD-{self.rover.current_step + 1}",
            action=action,
            arrival_step=self.rover.current_step + delay_steps,
        )
        return command

    def advance_time(self, steps=1):
        self.rover.current_step += steps

    def process_command(self, command):
        # A command cannot execute before its arrival time.
        if self.rover.current_step < command.arrival_step:
            return None

        before = (self.rover.x, self.rover.y)

        # Safety is checked against the rover's state NOW.
        safe, reason = check_command(self.rover, command)

        if safe:
            if command.action == "MOVE_FORWARD":
                self.rover.x += 1
                self.rover.battery -= 5

            elif command.action == "TAKE_PHOTO":
                self.rover.battery -= 2

            status = "ACCEPTED"
        else:
            status = "REJECTED"

        after = (self.rover.x, self.rover.y)

        return CommandResult(
            command_id=command.command_id,
            action=command.action,
            status=status,
            reason=reason,
            arrival_step=self.rover.current_step,
            position_before=before,
            position_after=after,
        )
