import base64

# Given base64 inputs - CHANGE IF DIFFERENT FOLLOW THE GUIDE :)

# this is the b64 encoded json format which you can find in the sourcecode (should never change, the format is constant)
plaintext_b64 = "eyJzaG93cGFzc3dvcmQiOiJubyIsImJnY29sb3IiOiIjZmZmZmZmIn0="

# this is the cookie that you need to copy from the storage tab
ciphertext_b64 = "HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg="

# Decode base64 inputs
plaintext = base64.b64decode(plaintext_b64)
ciphertext = base64.b64decode(ciphertext_b64)
xor_key = bytes([ciphertext[i] ^ plaintext[i] for i in range(len(plaintext))])

print("🔑 XOR Key Recovered:", xor_key)


# Repeating - dont need this just look at the xor_key and determine what's repeating
def detect_repeating_key(key):
    for i in range(1, len(key)):
        if (key[:i] * (len(key) // i + 1))[:len(key)] == key:
            return key[:i]
    return key

key = detect_repeating_key(xor_key)
# or 
# key = b'eDWo'
print("🧩 Likely Repeating Key:", key)

def xor_encrypt(data, key):
    return bytes([ord(data[i]) ^ key[i % len(key)] for i in range(len(data))])

# What we want to change to, showpass yes and change the background color so we see that is worked.
new_plaintext = '{"showpassword":"yes","bgcolor":"#000000"}'

# Step 1
encrypted = xor_encrypt(new_plaintext, key)

# Step 2
cookie_value = base64.b64encode(encrypted).decode()

print('\033[1m' + "Encrypted Cookie Value (set this as your 'data' cookie):", cookie_value)
