import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

_raw_admins = os.getenv("ADMINS")

if not _raw_admins:
    raise ValueError("ADMINS environment variable yo‘q yoki bo‘sh")

ADMINS = [int(x) for x in _raw_admins.split(",") if x.strip().isdigit()]

print("BOT_TOKEN:", BOT_TOKEN)
print("ADMINS:", ADMINS)
