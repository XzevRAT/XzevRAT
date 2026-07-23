@echo off
chcp 65001 >nul
echo Установка зависимостей для XzevRAT...
echo.
echo [1] Проверка наличия pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo Ошибка: pip не найден. Установите Python и добавьте pip в PATH.
    pause
    exit /b 1
)

echo [2] Установка зависимостей из requirements.txt...
pip install -r requirements.txt

echo.
echo ================================================
echo Готово! Все зависимости установлены.
echo ================================================
pause