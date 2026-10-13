\# 🚀 Mars Command Simulator

\### The Command That Arrived Too Late



A simulated Mars rover mission-control system that demonstrates why commands sent across long distances must be revalidated for safety when they arrive.



\## 🌌 The Problem



Commands sent from Earth to Mars experience communication delays. During that delay, the rover's environment can change. A movement command that was safe when sent may become dangerous by the time it arrives.



\## 💡 Our Solution



Mars Command Simulator models delayed command transmission and checks safety against the rover's \*\*current state at arrival time\*\*, rather than assuming the environment has stayed the same.



\## ✨ Features



\- \*\*Delayed command transmission\*\* — simulate communication delays.

\- \*\*Safety validation\*\* — reject movement into obstacles.

\- \*\*Battery checks\*\* — prevent actions when battery levels are insufficient.

\- \*\*Live mission dashboard\*\* — monitor rover position, battery, simulation time, and obstacles.

\- \*\*Command history\*\* — inspect command status and rejection reasons.

\- \*\*Interactive simulation\*\* — advance time, introduce obstacles, and reset the mission.



\## 🛠️ Tech Stack



\- Python

\- Streamlit

\- Pytest



\## 📁 Project Structure



```text

mars-command-simulator/

├── backend/

│   ├── engine.py

│   ├── models.py

│   └── safety.py

├── frontend/

│   └── app.py

├── tests/

│   └── test\_engine.py

├── requirements.txt

└── README.md

```



## Deploy to Streamlit Community Cloud

1. Push this repository to GitHub.
2. In [Streamlit Community Cloud](https://share.streamlit.io/), select **Create app** and connect the repository.
3. Select the branch containing this deployment setup and set the main file path to `streamlit_app.py`, then deploy.

Cloud installs the app dependencies from `requirements.txt`. No secrets or additional configuration are required.

\## ⚙️ Run Locally



\### 1. Clone the repository



```bash

git clone https://github.com/nehanazeer289-glitch/mars-command-simulator.git

cd mars-command-simulator

```



\### 2. Create and activate a virtual environment



\*\*Windows PowerShell:\*\*



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

```



\### 3. Install dependencies



```powershell

python -m pip install -r requirements.txt

```



\### 4. Launch the dashboard



```powershell

python -m streamlit run frontend/app.py

```



Open the local URL shown in your terminal, usually `http://localhost:8501`.



\## 🧪 Run Tests



```powershell

python -m pytest -v

```



The current automated test suite covers delayed command arrival and rejection of a movement command when an obstacle appears during transmission.



\## 🎬 Demo Scenario



1\. Reset the simulation.

2\. Transmit a `MOVE\_FORWARD` command.

3\. Introduce an obstacle at the rover's next position before the command arrives.

4\. Advance time until the command arrives.

5\. Observe the rejection and verify that the rover's position and battery remain unchanged.



\## 🔭 Future Improvements



\- Queue management for multiple commands.

\- More realistic communication-delay simulation.

\- Visual trajectory and telemetry history.

\- Additional safety rules and automated tests.



\---



\*\*Note:\*\* This is a local simulation for demonstration and educational purposes. It does not connect to a physical rover or a real Mars communication network.

