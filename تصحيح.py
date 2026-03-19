# save as debug.py and run it
from dotenv import load_dotenv
import os, hashlib

load_dotenv()
commit = os.getenv("COMMIT_HASH")
print(f"Raw value: {repr(commit)}")
print(f"Key hex: {hashlib.sha256(commit.strip().encode()).hexdigest()}")