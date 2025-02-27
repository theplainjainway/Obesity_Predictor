import os
import sys
import subprocess
import shutil

VENV_NAME = "env"
APP_SCRIPT = "app.py"
MODEL_SCRIPT = "model.py"

def run_command(command, shell=False):
    """Runs a command and handles errors."""
    try:
        subprocess.run(command, shell=shell, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        sys.exit(1)

def ensure_virtualenv():
    """Checks if virtualenv is installed, if not, installs it."""
    if not shutil.which("virtualenv"):
        print("virtualenv not found. Installing it...")
        run_command([sys.executable, "-m", "pip", "install", "virtualenv"])

def create_virtualenv():
    """Creates a virtual environment if it doesn't exist."""
    if not os.path.exists(VENV_NAME):
        print(f"Creating virtual environment: {VENV_NAME}...")
        run_command([sys.executable, "-m", "virtualenv", VENV_NAME])
    else:
        print(f"Virtual environment '{VENV_NAME}' already exists. Skipping creation.")

def get_pip_path():
    """Returns the path to the virtual environment's pip."""
    if os.name == "nt":
        return os.path.join(VENV_NAME, "Scripts", "pip.exe")
    else:
        return os.path.join(VENV_NAME, "bin", "pip")

def install_dependencies():
    """Installs required dependencies inside the virtual environment."""
    pip_path = get_pip_path()
    print("Installing dependencies...")
    run_command([pip_path, "install", "flask", "joblib", "numpy", "pandas", "scikit-learn", "requests"])

def set_execution_policy():
    """Sets execution policy for PowerShell (Windows only, scope: Process)."""
    if os.name == "nt":
        print("Setting PowerShell execution policy (Scope: Process)...")
        run_command(["powershell", "Set-ExecutionPolicy", "Unrestricted", "-Scope", "Process", "-Force"], shell=True)

def get_activate_command():
    """Returns the correct virtual environment activation command."""
    if os.name == "nt":
        return f"{VENV_NAME}\\Scripts\\activate"
    else:
        return f"source {VENV_NAME}/bin/activate"

def run_script_in_new_terminal(script_name):
    """Runs a Python script in a new terminal with the virtual environment activated."""
    activation_cmd = get_activate_command()

    if os.name == "nt":
        command = f'powershell -NoExit -Command "Set-ExecutionPolicy Unrestricted -Scope Process -Force; {activation_cmd}; python {script_name}"'
        subprocess.Popen(["powershell", "-NoExit", "-Command", command], shell=True)
    else:
        command = f'gnome-terminal -- bash -c "{activation_cmd} && python {script_name}; exec bash"'
        subprocess.Popen(command, shell=True)

if __name__ == "__main__":
    print(f"Detected OS: {'Windows' if os.name == 'nt' else 'Linux/macOS'}")

    set_execution_policy()  # Windows only
    ensure_virtualenv()
    create_virtualenv()
    install_dependencies()

    print("\nVirtual environment setup is complete! 🎉")
    print(f"To activate it, run:\n{VENV_NAME}\\Scripts\\activate" if os.name == "nt" else f"source {VENV_NAME}/bin/activate")

    print("\nStarting model.py in a new terminal...")
    run_script_in_new_terminal(MODEL_SCRIPT)

    print("Starting app.py in a new terminal...")
    run_script_in_new_terminal(APP_SCRIPT)

    print("\nBoth scripts are running in separate terminals! 🚀")
