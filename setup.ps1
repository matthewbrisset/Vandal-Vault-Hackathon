# Vandal Vault - Setup Script for Windows (PowerShell)
$pythonCheck = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "[*] Creating virtual environment..."
    if (-Not (Test-Path "venv")) {
        python -m venv venv
    }
    
    Write-Host "[*] Activating virtual environment..."
    & ".\venv\Scripts\Activate.ps1"
    
    Write-Host "[*] Installing dependencies..."
    pip install -r requirements.txt
    
    Write-Host "[*] Verifying pytest installation..."
    pytest --version
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[!] pytest not found. Installing explicitly..."
        pip install pytest
    }
    
    Write-Host "[*] Setting up environment..."
    if (-Not (Test-Path ".env")) {
        Copy-Item ".env.example" ".env"
        Write-Host "[+] Created .env file - add your GROQ_API_KEY"
    }
    
    Write-Host ""
    Write-Host "Setup complete!"
    Write-Host "Next: Add GROQ_API_KEY to .env and run pytest tests/test_user_advice_generator.py -v -s"
    Write-Host ""
} else {
    Write-Host "Python not found. Install Python 3.9+ first."
    exit 1
}
