import os
from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR = "/home/du"
load_dotenv(dotenv_path=f"{BASE_DIR}/.env")

# KIWI_API_KEY=<key> in Datei .env speichern

client = OpenAI(
    api_key=os.getenv("KIWI_API_KEY"),
    base_url="https://f2ki-h100-1.f2.htw-berlin.de:11435/v1"
)

response = client.chat.completions.create(
    model="qwen3.8-27b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Was ist die Hauptstadt von Deutschland?"}
    ]
)

print(response.choices[0].message.content)