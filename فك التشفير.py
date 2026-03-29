import hashlib, wave
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
from dotenv import load_dotenv
import os

load_dotenv()

def get_repo_key():
    commit = os.getenv("COMMIT_HASH")
    if not commit:
        print("Missing required configuration.")
        exit(1)
    return hashlib.sha256(commit.strip().encode()).digest()

def decode_audio(wav_file: str) -> str:
    with wave.open(wav_file, 'rb') as f:
        frames = bytearray(f.readframes(f.getnframes()))

    bits = [str(frame & 1) for frame in frames]
    chars = []
    for i in range(0, len(bits) - 8, 8):
        byte = ''.join(bits[i:i+8])
        char = chr(int(byte, 2))
        chars.append(char)
        if ''.join(chars[-9:]) == "###END###":
            return ''.join(chars[:-9])

    raise ValueError("Invalid input.")

def decrypt_message(encrypted: str, key: bytes) -> str:
    raw = b64decode(encrypted)
    iv, ct = raw[:16], raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    return unpad(cipher.decrypt(ct), 16).decode()

if __name__ == "__main__":
    import sys
    wav_file = sys.argv[1] if len(sys.argv) > 1 else "temple_encoded.wav"

    key = get_repo_key()
    encrypted = decode_audio(wav_file)
    hint = decrypt_message(encrypted, key)

    print(hint)
    