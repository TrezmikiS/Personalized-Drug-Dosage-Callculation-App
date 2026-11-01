@echo off
chcp 65001 >nul
title Klinik Doz Hesaplama Uygulaması

echo ================================================================
echo   Kişiselleştirilmiş İlaç Dozu Hesaplama Uygulaması (FE401)
echo ================================================================
echo.
echo [1/3] Backend (FastAPI) sunucusu başlatılıyor (Port 8000)...
start "Pharmacy Backend (FastAPI)" cmd /k "cd /d "%~dp0" && .\backend\venv\Scripts\uvicorn.exe backend.app.main:app --port 8000"

echo [2/3] Frontend (React + Vite) sunucusu başlatılıyor (Port 5173)...
start "Pharmacy Frontend (React)" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo [3/3] Sunucuların hazır olması bekleniyor ve tarayıcı açılıyor...
timeout /t 4 /nobreak >nul

:: Başlangıç dar terapötik ilaçlarını (Vankomisin, Digoksin, Lityum) otomatik tohumla (seed)
powershell -Command "try { Invoke-RestMethod -Uri http://localhost:8000/api/seed-drugs -Method Post -ErrorAction SilentlyContinue } catch {}" >nul 2>&1

:: Tarayıcıyı otomatik olarak aç
start http://localhost:5173

echo.
echo ================================================================
echo  ✅ Uygulama başarıyla başlatıldı!
echo  🌐 Web Arayüzü : http://localhost:5173
echo  📚 API Docs    : http://localhost:8000/docs
echo.
echo  Pencereleri kapatarak uygulamayı dilediğiniz zaman durdurabilirsiniz.
echo ================================================================
echo.
pause
