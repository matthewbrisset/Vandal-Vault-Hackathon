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
    Write-Host "Next steps:"
    Write-Host "  1. Add GROQ_API_KEY to .env"
    Write-Host "  2. Run tests: pytest tests/ -v"
    Write-Host "  3. Start Flask server: python -m src.Backend.app"
    Write-Host "  4. Open http://localhost:5000 in your browser"
    Write-Host ""
} else {
    Write-Host "Python not found. Install Python 3.9+ first."
    exit 1
}
