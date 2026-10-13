
import streamlit as st
import pandas as pd
from backend.engine import RoverEngine
from backend.models import RoverState

st.set_page_config(
    page_title="Mars Mission Control",
    page_icon="🚀",
    layout="wide",
)

st.markdown("""
<style>
.stApp { background: #0b1020; color: #e8edf8; }
h1, h2, h3 { color: #e8edf8; }
[data-testid="stMetric"] {
    background: #151d32;
    border: 1px solid #293653;
    padding: 16px;
    border-radius: 12px;
}
div.stButton > button {
    width: 100%;
    border-radius: 9px;
    min-height: 44px;
}
</style>
""", unsafe_allow_html=True)


def create_engine():
    return RoverEngine(RoverState(obstacles=[(3, 0)]))


if "engine" not in st.session_state:
    st.session_state.engine = create_engine()
if "pending" not in st.session_state:
    st.session_state.pending = []
if "history" not in st.session_state:
    st.session_state.history = []
if "route" not in st.session_state:
    st.session_state.route = [(0, 0)]
if "next_id" not in st.session_state:
    st.session_state.next_id = 1

engine = st.session_state.engine
rover = engine.rover


def process_arrived_commands():
    arrived = [
        cmd for cmd in st.session_state.pending
        if cmd.arrival_step <= rover.current_step
    ]

    for command in arrived:
        result = engine.process_command(command)

        for item in st.session_state.history:
            if item["Command"] == command.command_id:
                item["Status"] = result.status
                item["Reason"] = result.reason
                item["Position after"] = str(result.position_after)
                break

        if result.position_after != result.position_before:
            st.session_state.route.append(result.position_after)

        st.session_state.pending.remove(command)


def send_command(action, delay):
    command = engine.send_command(action, delay_steps=delay)
    command.command_id = f"CMD-{st.session_state.next_id:03}"
    st.session_state.next_id += 1

    st.session_state.pending.append(command)
    st.session_state.history.insert(0, {
        "Command": command.command_id,
        "Action": action,
        "Status": "PENDING",
        "Reason": f"Arrives at step {command.arrival_step}",
        "Position after": "Awaiting arrival",
    })


st.title("🚀 MARS MISSION CONTROL")
st.caption("COMMAND TRANSMISSION SYSTEM / MARS ROVER SIMULATOR")
st.divider()

a, b, c, d = st.columns(4)
a.metric("ROVER POSITION", f"({rover.x}, {rover.y})")
b.metric("BATTERY", f"{rover.battery}%")
c.metric("SIMULATION STEP", rover.current_step)
d.metric("OBSTACLES", len(rover.obstacles))

st.subheader("Command uplink")
delay = st.slider("Simulated transmission delay (steps)", 1, 5, 2)

left, right = st.columns(2)

with left:
    if st.button("⬆️ TRANSMIT: MOVE FORWARD"):
        send_command("MOVE_FORWARD", delay)
        st.rerun()

with right:
    if st.button("📸 TRANSMIT: TAKE PHOTO"):
        send_command("TAKE_PHOTO", delay)
        st.rerun()

st.caption(
    "Commands are evaluated against the rover's current state upon arrival."
)

x, y = st.columns(2)

with x:
    st.subheader("Simulation controls")

    if st.button("⏩ Advance time by 1 step"):
        engine.advance_time(1)
        process_arrived_commands()
        st.rerun()

    if st.button("⏩⏩ Advance time until next arrival"):
        if st.session_state.pending:
            next_step = min(
                cmd.arrival_step for cmd in st.session_state.pending
            )
            engine.advance_time(
                max(0, next_step - rover.current_step)
            )
            process_arrived_commands()
            st.rerun()
        else:
            st.info("No commands are currently in transit.")

    if st.button("⚠️ Introduce obstacle at next position"):
        obstacle = (rover.x + 1, rover.y)

        if obstacle not in rover.obstacles:
            rover.obstacles.append(obstacle)
            st.session_state.last_notice = (
                f"Obstacle introduced at {obstacle}."
            )
        else:
            st.session_state.last_notice = (
                f"An obstacle already exists at {obstacle}."
            )

        st.rerun()

    if st.session_state.get("last_notice"):
        st.warning(st.session_state.last_notice)

    if st.button("🔄 Reset simulation"):
        st.session_state.engine = create_engine()
        st.session_state.pending = []
        st.session_state.history = []
        st.session_state.route = [(0, 0)]
        st.session_state.next_id = 1
        st.session_state.last_notice = ""
        st.rerun()

with y:
    st.subheader("Rover surface map")

    map_data = pd.DataFrame(
        st.session_state.route,
        columns=["x", "y"],
    )
    st.line_chart(map_data, x="x", y="y")

    st.caption("Route history: each point represents a rover position.")

    st.subheader("Terrain grid")
    for row in range(2, -1, -1):
        line = []
        for col in range(7):
            if (col, row) == (rover.x, rover.y):
                line.append("🛰️")
            elif (col, row) in rover.obstacles:
                line.append("🪨")
            else:
                line.append("▫️")
        st.code(" ".join(line), language=None)

    st.caption("🛰️ Rover   🪨 Obstacle   ▫️ Clear terrain")

st.divider()
st.subheader("Command queue")

if st.session_state.pending:
    queue_rows = []
    for cmd in st.session_state.pending:
        queue_rows.append({
            "Command": cmd.command_id,
            "Action": cmd.action,
            "Arrival step": cmd.arrival_step,
            "Steps remaining": max(
                0, cmd.arrival_step - rover.current_step
            ),
            "Status": "IN TRANSIT",
        })
    st.dataframe(
        queue_rows,
        width="stretch",
        hide_index=True,
    )
else:
    st.info("No commands currently in transit.")

st.subheader("Command transmission timeline")

if st.session_state.history:
    st.dataframe(
        st.session_state.history,
        width="stretch",
        hide_index=True,
    )
else:
    st.info("No commands sent yet. Transmit your first command above.")

st.caption(
    "SIMULATED ENVIRONMENT • Local simulation • No real rover connection"
)
