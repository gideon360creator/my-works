# Single-shell launcher for Windows PowerShell
# Place this file in the project root (already done).
# Usage (PowerShell):
#   .\start.ps1
# This script will:
# - Create a Python virtual environment at .venv if it doesn't exist
# - Activate the venv for the current session
# - Run `python run.py` which launches both backend (uvicorn) and frontend (Vite)

param(
    [switch]$NoCreateVenv
)

# Resolve project root
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ProjectRoot

# Ensure python exists
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Error "Python is not available on PATH. Please install Python and try again."
    exit 1
}

$venvPath = Join-Path $ProjectRoot ".venv"

if (-not (Test-Path $venvPath)) {
    if ($NoCreateVenv) {
        Write-Host ".venv not found and -NoCreateVenv specified. Continuing without virtual environment." -ForegroundColor Yellow
    } else {
        Write-Host "Creating virtual environment at $venvPath..."
        python -m venv .venv
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to create virtual environment."
            exit 1
        }
        Write-Host "Virtual environment created."
    }
} else {
    Write-Host "Using existing virtual environment at $venvPath"
}

# Activate venv for the current session (if present)
$activateScript = Join-Path $venvPath "Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    Write-Host "Activating virtual environment..."
    # dot-source the activation script so the session is modified
    . $activateScript
} else {
    Write-Host "No activation script found; continuing without activating venv." -ForegroundColor Yellow
}

# Run the Python runner which starts both backend and frontend
Write-Host "Starting project (backend + frontend) via run.py..."
python run.py

# When run.py exits, script will return here
Write-Host "Launcher exiting."