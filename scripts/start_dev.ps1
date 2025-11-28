# PowerShell helper to start the project in a virtual environment
# Usage: Open PowerShell in project root and run: .\scripts\start_dev.ps1

$venvPath = "$PSScriptRoot\..\.venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    Write-Host "Activating venv..."
    & $venvPath
} else {
    Write-Host "No .venv found. Creating one..."
    python -m venv .venv
    & "$PSScriptRoot\..\.venv\Scripts\Activate.ps1"
    pip install -r "$PSScriptRoot\..\requirements.txt"
}

Write-Host "Starting Flask app..."
python "$PSScriptRoot\..\app.py"
