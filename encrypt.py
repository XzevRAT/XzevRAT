import base64

# ←←← СЮДА ВСТАВЬ СВОИ ДАННЫЕ ←←←
bot_token = ""
chat_id = ""

# Шифрование
encrypted_token = base64.b64encode(bot_token.encode('utf-8')).decode('utf-8')
encrypted_chat = base64.b64encode(chat_id.encode('utf-8')).decode('utf-8')

print("encrypted_token =", encrypted_token)
print("encrypted_chat =", encrypted_chat)