# Check for Python
$pythonVersion = python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Python is not installed or not in PATH." -ForegroundColor Red
    exit 1
}
Write-Host "Found $($pythonVersion)" -ForegroundColor Green

# Check for Docker
$dockerVersion = docker --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker is not installed or not in PATH." -ForegroundColor Yellow
    Write-Host "You can still run backend tests locally, but full stack won't run." -ForegroundColor Yellow
} else {
    Write-Host "Found $($dockerVersion)" -ForegroundColor Green
}

# Create Virtual Environment for Backend
$venvPath = "backend\venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating Python virtual environment in $venvPath..."
    python -m venv $venvPath
} else {
    Write-Host "Virtual environment already exists in $venvPath."
}

# Install Requirements
Write-Host "Installing backend requirements..."
& ".\$venvPath\Scripts\pip" install -r backend\requirements.txt
& ".\$venvPath\Scripts\pip" install pytest pytest-asyncio grpcio-tools

Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "To activate the virtual environment, run: .\backend\venv\Scripts\Activate.ps1"
