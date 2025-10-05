@echo off
echo =====================================
echo Copie des assets pour TerraGrow 3D
echo =====================================
echo.

REM Créer les dossiers si nécessaire
if not exist "public\textures" mkdir public\textures
if not exist "public\models" mkdir public\models

echo Copie des textures Earth...
copy "..\glb\2k_earth_daymap.jpg" "public\textures\" /Y
copy "..\glb\2k_earth_nightmap.jpg" "public\textures\" /Y
copy "..\glb\2k_earth_clouds.jpg" "public\textures\" /Y
copy "..\glb\2k_stars.jpg" "public\textures\" /Y

echo.
echo Copie du modèle satellite...
copy "..\glb\satellite.glb" "public\models\" /Y

echo.
echo =====================================
echo Assets copiés avec succès!
echo =====================================
echo.
echo Fichiers copiés:
echo   - public/textures/2k_earth_daymap.jpg
echo   - public/textures/2k_earth_nightmap.jpg
echo   - public/textures/2k_earth_clouds.jpg
echo   - public/textures/2k_stars.jpg
echo   - public/models/satellite.glb
echo.
echo Vous pouvez maintenant lancer: npm run dev
echo.
pause
