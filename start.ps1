# LandslideGuard AI - PowerShell Launcher
$env:PATH = "C:\Program Files\nodejs;" + $env:PATH

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Starting LandslideGuard AI System" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Cyan

Write-Host "[1/2] Launching FastAPI Backend on http://127.0.0.1:8000 ..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload"

Write-Host "[2/2] Launching Vite React Dashboard on http://localhost:5173 ..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:PATH = 'C:\Program Files\nodejs;' + `$env:PATH; cd frontend; npm run dev"

Write-Host ""
Write-Host "Both servers launched successfully!" -ForegroundColor Green
Write-Host "Dashboard: http://localhost:5173" -ForegroundColor White
Write-Host "API Docs:  http://127.0.0.1:8000/docs" -ForegroundColor White
