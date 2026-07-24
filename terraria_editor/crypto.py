import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Terraria AES Encryption Keys
# Key 1: "68332866" repeated to 16 bytes (as specified in prompt: 68 33 28 66)
KEY_68332866 = b"6833286668332866"

# Key 2: Standard Terraria UTF-16 LE "h3y_gUyZ"
KEY_H3Y_GUYZ = "h3y_gUyZ".encode("utf-16le")

def decrypt_plr(data: bytes) -> tuple[bytes, bytes]:
    """
    Attempts to decrypt a .plr binary buffer using known Terraria AES-128 keys.
    Returns a tuple: (decrypted_bytes, key_used)
    """
    keys = [KEY_68332866, KEY_H3Y_GUYZ]
    
    # Check if file is already unencrypted (starts with length byte + "relogic")
    if len(data) > 8 and b"relogic" in data[:20]:
        return data, KEY_68332866

    for key in keys:
        try:
            cipher = AES.new(key, AES.MODE_CBC, iv=key)
            decrypted = cipher.decrypt(data)
            # Try unpadding
            try:
                unpadded = unpad(decrypted, AES.block_size)
            except Exception:
                unpadded = decrypted
            
            # Check for magic header "relogic"
            if len(unpadded) > 7 and b"relogic" in unpadded[:20]:
                return unpadded, key
        except Exception:
            continue
            
    # If magic header not found by standard unpadding, try raw decryption check
    for key in keys:
        try:
            cipher = AES.new(key, AES.MODE_CBC, iv=key)
            decrypted = cipher.decrypt(data)
            if len(decrypted) > 7 and b"relogic" in decrypted[:20]:
                return decrypted, key
        except Exception:
            continue

    raise ValueError("Failed to decrypt .plr file. Invalid format or unsupported encryption key.")

def encrypt_plr(data: bytes, key: bytes = KEY_68332866) -> bytes:
    """
    Encrypts raw .plr byte data using AES-128-CBC with PKCS7 padding.
    """
    cipher = AES.new(key, AES.MODE_CBC, iv=key)
    padded_data = pad(data, AES.block_size)
    return cipher.encrypt(padded_data)
