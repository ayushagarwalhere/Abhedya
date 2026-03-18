import subprocess, hashlib, wave
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode

# --- Step 1: Reproduce the same key from this repo ---
def get_repo_key():
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL
        ).strip()
        return hashlib.sha256(commit).digest()
    except Exception:
        print("[!] ERROR: You must run this inside the cloned repository.")
        print("    The key is bound to this repo's commit history.")
        exit(1)

# --- Step 2: Extract hidden bits from WAV ---
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

    raise ValueError("[!] No hidden message found — wrong file or corrupted audio.")

# --- Step 3: Decrypt ---
def decrypt_message(encrypted: str, key: bytes) -> str:
    raw = b64decode(encrypted)
    iv, ct = raw[:16], raw[16:]
    cipher = AES.new(key, AES.MODE_CBC)
    return unpad(cipher.decrypt(ct), 16).decode()

# --- Run ---
if __name__ == "__main__":
    import sys
    wav_file = sys.argv[1] if len(sys.argv) > 1 else "temple_encoded.wav"

    print(f"[~] The priests consult the sacred file: {wav_file}")
    print("[~] Reconstructing the key from the tomb's memory...")

    key = get_repo_key()
    encrypted = decode_audio(wav_file)
    hint = decrypt_message(encrypted, key)

    print("\n═══════════════════════════════════════════")
    print("  THE INSCRIPTION READS:")
    print(f"\n  {hint}\n")
    print("═══════════════════════════════════════════\n")
    