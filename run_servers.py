import subprocess
import sys
import os
import time

DETACHED = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP

base_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(base_dir, "frontend")
node_dir = r"C:\Program Files\nodejs"

env = os.environ.copy()
env["PATH"] = node_dir + ";" + env.get("PATH", "")

backend_log = open(os.path.join(base_dir, "backend.log"), "w")
frontend_log = open(os.path.join(base_dir, "frontend.log"), "w")

# Launch FastAPI backend
backend_proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
    cwd=base_dir,
    env=env,
    stdout=backend_log,
    stderr=subprocess.STDOUT,
    creationflags=DETACHED
)

# Launch React Vite frontend
frontend_proc = subprocess.Popen(
    [os.path.join(node_dir, "npm.cmd"), "run", "dev"],
    cwd=frontend_dir,
    env=env,
    stdout=frontend_log,
    stderr=subprocess.STDOUT,
    creationflags=DETACHED
)

print(f"FastAPI Backend PID: {backend_proc.pid} (logging to backend.log)")
print(f"React Frontend PID: {frontend_proc.pid} (logging to frontend.log)")

# Give servers 4 seconds to initialize
time.sleep(4)
