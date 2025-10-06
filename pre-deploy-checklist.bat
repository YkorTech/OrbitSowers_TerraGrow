@echo off
REM Pre-deployment checklist for TerraGrow Academy (Windows)

echo.
echo ===========================================
echo TerraGrow Academy - Pre-Deployment Check
echo ===========================================
echo.

REM Check 1: render.yaml
echo Checking render.yaml...
if exist "render.yaml" (
    echo   [OK] render.yaml found
) else (
    echo   [ERROR] render.yaml NOT FOUND
    exit /b 1
)

REM Check 2: Backend requirements
echo.
echo Checking backend requirements...
if exist "backend\requirements.txt" (
    echo   [OK] requirements.txt found
    findstr /C:"gunicorn" backend\requirements.txt >nul
    if %errorlevel% equ 0 (
        echo   [OK] gunicorn is present
    ) else (
        echo   [ERROR] gunicorn missing in requirements.txt
        exit /b 1
    )
) else (
    echo   [ERROR] backend\requirements.txt NOT FOUND
    exit /b 1
)

REM Check 3: Frontend package.json
echo.
echo Checking frontend configuration...
if exist "frontend\package.json" (
    echo   [OK] package.json found
    findstr /C:"build" frontend\package.json >nul
    if %errorlevel% equ 0 (
        echo   [OK] build script present
    ) else (
        echo   [ERROR] build script missing
        exit /b 1
    )
) else (
    echo   [ERROR] frontend\package.json NOT FOUND
    exit /b 1
)

REM Check 4: API client
echo.
echo Checking API client...
if exist "frontend\src\utils\apiClient.js" (
    echo   [OK] apiClient.js found
    findstr /C:"VITE_API_URL" frontend\src\utils\apiClient.js >nul
    if %errorlevel% equ 0 (
        echo   [OK] Uses VITE_API_URL environment variable
    ) else (
        echo   [WARNING] Not using VITE_API_URL
    )
) else (
    echo   [ERROR] apiClient.js NOT FOUND
    exit /b 1
)

REM Check 5: .gitignore
echo.
echo Checking .gitignore...
if exist ".gitignore" (
    echo   [OK] .gitignore found
) else (
    echo   [WARNING] .gitignore not found
)

REM Check 6: Documentation
echo.
echo Checking documentation...
if exist "DEPLOYMENT.md" (
    echo   [OK] DEPLOYMENT.md present
)
if exist "QUICKSTART.md" (
    echo   [OK] QUICKSTART.md present
)
if exist "README.md" (
    echo   [OK] README.md present
)

echo.
echo ===========================================
echo Pre-deployment check COMPLETE!
echo ===========================================
echo.
echo Next steps:
echo 1. git add .
echo 2. git commit -m "Add deployment configuration"
echo 3. git push origin main
echo 4. Go to https://render.com and deploy!
echo.
pause
