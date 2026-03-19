import subprocess, hashlib, wave
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode

def get_repo_key():
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip()
    print(f"[~] Encoding with commit: {commit.decode()}")
    return hashlib.sha256(commit).digest()

def encrypt_message(message: str, key: bytes) -> str:
    cipher = AES.new(key, AES.MODE_CBC)
    ct = cipher.encrypt(pad(message.encode(), 16))
    return b64encode(cipher.iv + ct).decode()

def encode_audio(input_wav: str, output_wav: str, secret: str):
    data = (secret + "###END###").encode()
    bits = ''.join(format(b, '08b') for b in data)

    with wave.open(input_wav, 'rb') as f:
        frames = bytearray(f.readframes(f.getnframes()))
        params = f.getparams()

    if len(bits) > len(frames):
        raise ValueError("Message too long for this audio file! Use a longer WAV.")

    for i, bit in enumerate(bits):
        frames[i] = (frames[i] & ~1) | int(bit)

    with wave.open(output_wav, 'wb') as f:
        f.setparams(params)
        f.writeframes(bytes(frames))

    print(f"[+] The secret has been sealed into → {output_wav}")

if __name__ == "__main__":
    key = get_repo_key()
    hint = (
        "The alchemists chased   the king of metals believing the sun itself slept within it "
        "When the lion of light awakens the secret of the philosophers reveals its name"
    )
    encrypted = encrypt_message(hint, key)
    encode_audio("temple.wav", "temple_encoded.wav", encrypted)