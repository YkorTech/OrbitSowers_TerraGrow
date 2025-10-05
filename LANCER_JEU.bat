@echo off
echo ========================================
echo    TERRAGROW ACADEMY - LANCEMENT
echo ========================================
echo.

echo [1] Demarrage du backend...
start "TerraGrow Backend" cmd /k "cd backend && python app.py"
timeout /t 3 >nul

echo [2] Demarrage du frontend...
start "TerraGrow Frontend" cmd /k "cd frontend && python -m http.server 8000"
timeout /t 2 >nul

echo [3] Ouverture dans le navigateur...
start http://localhost:8000

echo.
echo ========================================
echo    JEU LANCE !
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:8000
echo.
echo Appuyez sur une touche pour fermer cette fenetre...
pause >nul
