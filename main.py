from telethon import TelegramClient, events
from telethon.sessions import StringSession
import os
import requests
import asyncio

# Telegram API credentials (from my.telegram.org)
API_ID = int(os.environ['API_ID']) # Telegram API ID
API_HASH = os.environ['API_HASH'] # Telegram API Hash
STRING_SESSION = os.environ['STRING_SESSION'] # String Session

# OpenRouter API credentials
API_KEY = os.environ['API_KEY'] # Translation API Key
API_URL = "https://openrouter.ai/api/v1/chat/completions"


SOURCE_CHANNEL = int(os.environ['SOURCE_CHANNEL']) # Source Channel ID
TARGET_CHANNEL = int(os.environ['TARGET_CHANNEL']) # Target Channel ID



# DeepSeek translation function
def deepseek_translate(message, src='en', dest='my'):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-type": "application/json"}
    data = {
        "model": "deepseek/deepseek-chat",
        "messages": [
            {"role": "system", "content": "Translate English to Burmese in a natural tone."},
            {"role": "user", "content": message}
        ]
    }
    
    res = requests.post(API_URL, json=data, headers=headers)
    res_json = res.json()
    if "choices" in res_json:
        return res_json["choices"][0]["message"]["content"]
    else:
        return f"Error: {res_json}"
    

# Connect to Telegram
client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
async def main():
    # Login to Telegram
    await client.start()
    print("User logged in!")
    
    # send a startup message to the target channel
    await client.send_message(TARGET_CHANNEL, "🤖 Bot started and listening for new messages...")
    print("Startup message sent to target channel and listening new messages!")
    
    # Listen to source channel messages
    @client.on(events.NewMessage(from_users = SOURCE_CHANNEL))
    async def handler(event):
        message_text = event.message.message
        print("New message!")
        if message_text:
            try:
                translated_text = deepseek_translate(message_text) # Translate message
                print("Message translated!")
                await client.send_message(TARGET_CHANNEL, translated_text)  # Send to target channel
                print("Message sent to target channel!")
            except Exception as e:
                print("Error:", e)
        
    await client.run_until_disconnected()

# Run the script
if __name__ == "__main__":
    asyncio.run(main())