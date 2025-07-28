import base64

# Given base64 inputs - CHANGE IF DIFFERENT FOLLOW THE GUIDE :)
plaintext_b64 = "eyJzaG93cGFzc3dvcmQiOiJubyIsImJnY29sb3IiOiIjZmZmZmZmIn0="
ciphertext_b64 = "HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg="
new_plaintext = '{"showpassword":"yes","bgcolor":"#ffffff"}'

# Decode base64 inputs
plaintext = base64.b64decode(plaintext_b64)
ciphertext = base64.b64decode(ciphertext_b64)

xor_key = bytes([ciphertext[i] ^ plaintext[i] for i in range(len(plaintext))])

print("🔑 XOR Key Recovered:", xor_key)

def detect_repeating_key(key):
    for i in range(1, len(key)):
        if (key[:i] * (len(key) // i + 1))[:len(key)] == key:
            return key[:i]
    return key

key = detect_repeating_key(xor_key)
print("🧩 Likely Repeating Key:", key)

def xor_encrypt(data, key):
    return bytes([ord(data[i]) ^ key[i % len(key)] for i in range(len(data))])

encrypted = xor_encrypt(new_plaintext, key)
cookie_value = base64.b64encode(encrypted).decode()

print("\n Encrypted Cookie Value (set this as your 'data' cookie):")
print(cookie_value)
