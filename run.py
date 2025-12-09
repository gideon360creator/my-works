import subprocess
import time
import webbrowser
import os
import sys
import shutil
import importlib.util

def main():
    print("Starting Student Performance Chatbot System...")

    # Paths
    project_root = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(project_root, "backend")
    frontend_dir = os.path.join(project_root, "frontend")

    backend_process = None
    frontend_process = None

    # Start Backend
    print("Launching Backend (FastAPI)...")
    try:
        backend_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
            cwd=backend_dir,
            shell=False
        )
    except FileNotFoundError as e:
        print(f"Failed to start backend process: {e}")
        print("Make sure Python is installed and available on PATH.")
        backend_process = None
    except Exception as e:
        # If uvicorn module isn't available, try installing requirements automatically (best-effort)
        print(f"Backend failed to start: {e}")
        backend_process = None
        uvicorn_spec = importlib.util.find_spec("uvicorn")
        if uvicorn_spec is None:
            reqs = os.path.join(backend_dir, "requirements.txt")
            if os.path.exists(reqs):
                print("uvicorn not found in the current Python environment. Attempting to install backend requirements...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", reqs])
                    print("Requirements installed. Retrying backend start...")
                    backend_process = subprocess.Popen(
                        [sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
                        cwd=backend_dir,
                        shell=False
                    )
                except Exception as ie:
                    print(f"Automatic install failed: {ie}")
                    print(f"Please install requirements manually: python -m pip install -r {reqs}")
            else:
                print("No requirements.txt found in backend; please install uvicorn manually into your Python environment.")

    # Start Frontend
    print("Launching Frontend (Vite)...")
    # Use npm.cmd on Windows to avoid PowerShell .ps1 execution policy problems
    npm_cmd = "npm"
    if sys.platform == "win32":
        npm_cmd = "npm.cmd"

    npm_path = shutil.which(npm_cmd)
    if not npm_path:
        print(f"Warning: '{npm_cmd}' not found on PATH. Frontend will not be started by this script.")
        print("If you want to run the frontend, install Node.js (which provides npm) or run 'npm run dev' in the frontend folder manually.")
        frontend_process = None
    else:
        try:
            frontend_process = subprocess.Popen(
                [npm_cmd, "run", "dev"],
                cwd=frontend_dir,
                shell=False
            )
        except Exception as e:
            print(f"Failed to start frontend process: {e}")
            frontend_process = None

    # Open Browser (only if a server is running)
    print("Opening Browser...")
    time.sleep(4)  # Wait a few seconds for servers to initialize
    if frontend_process and frontend_process.poll() is None:
        webbrowser.open("http://localhost:5173")
    elif backend_process and backend_process.poll() is None:
        webbrowser.open("http://localhost:8000")
    else:
        print("No running server found to open in browser.")

    print("\nSystem is running!")
    print("   Backend API: http://localhost:8000")
    print("   Frontend App: http://localhost:5173")
    print("   Press Ctrl+C to stop both servers.")

    try:
        # Keep the script running to monitor processes
        while True:
            time.sleep(1)
            if backend_process and backend_process.poll() is not None:
                print("Backend process ended unexpectedly.")
                break
            if frontend_process and frontend_process.poll() is not None:
                print("Frontend process ended unexpectedly.")
                break
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")

        def _kill_proc(proc):
            if not proc:
                return
            try:
                if sys.platform == "win32":
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    proc.terminate()
                    time.sleep(0.5)
                    if proc.poll() is None:
                        proc.kill()
            except Exception:
                try:
                    proc.kill()
                except Exception:
                    pass

        _kill_proc(frontend_process)
        _kill_proc(backend_process)

        print("Goodbye!")

if __name__ == "__main__":
    main()
