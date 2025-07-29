# 🔐 Natas11 Walkthrough

On this level, we are introduced to XOR encryption — a reversible encryption process, **as long as you have the key**. The easiest way to recover a key used in XOR encryption is to obtain:

- The encrypted data
- The data before encryption (plaintext)

That way, we can determine the key by comparing the two. Let’s see what the [View sourcecode](http://natas11.natas.labs.overthewire.org/index-source.html) reveals.



### 🔧 XOR Encrypt Function

This is the function used for encryption:
```php
function xor_encrypt($in) {
    $key = '<censored>';
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
        $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}
```

Looking further down, we can see that the `saveData()` function saves the `"data"` cookie after:

1. Encoding a JSON object: `{"showpassword":"no", "bgcolor":"#ffffff"}`
2. Encrypting it with XOR
3. Encoding the result with Base64

This gives us exactly what we need:
- ✅ **Plaintext** — we know the default data structure
- ✅ **Ciphertext** — we can extract it from the `data` cookie



## 🧪 Step-by-step Plan:

### 1. **Get the Encrypted Cookie (Ciphertext)**

Inspect the page (Right click → Inspect → Storage → Cookies) and you’ll find a cookie like:

```
data=HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg%3D
```

This cookie is Base64 encoded, but notice the `%3D` at the end — that's just a URL-encoded `=`.

So we decode this:
```
HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg=
```

✅ **This is our ciphertext ^**

Let’s decode it in Python:
```python
import base64

cookie = "HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg="
decoded = base64.b64decode(cookie)
print(decoded)
```

You should get something like:
```
b'\x1ef$\x07\n3\'\x0e\x167 \x00\x17 uUG*8MIf5\x08\x06+;\x00\x17fmMF"1\t\x03"1M\x18'
```



### 2. **Get the Known Plaintext**

From the source code, we know the original data:
```json
{"showpassword":"no","bgcolor":"#ffffff"}
```

Let’s Base64 encode that in Python (just to verify structure):
```python
import base64

plaintext = b'{"showpassword":"no","bgcolor":"#ffffff"}'
encoded = base64.b64encode(plaintext)
print(encoded)
```

You should get:
```
b'eyJzaG93cGFzc3dvcmQiOiJubyIsImJnY29sb3IiOiIjZmZmZmZmIn0='
```

✅ **This is the encoded plaintext ^**



### 3. **Recover the XOR Key**

Now XOR the ciphertext with the known plaintext to recover the key:
```python
import base64

plaintext_b64 = "eyJzaG93cGFzc3dvcmQiOiJubyIsImJnY29sb3IiOiIjZmZmZmZmIn0="
ciphertext_b64 = "HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg="

plaintext = base64.b64decode(plaintext_b64)
ciphertext = base64.b64decode(ciphertext_b64)

xor_key = bytes([ciphertext[i] ^ plaintext[i] for i in range(len(plaintext))])

print("🔑 XOR Key Recovered:", xor_key)
```

Output:
```
b'eDWoeDWoeDWoeDWoeDWoeDWoeDWoeDWoeDWoeDWoe'
```

Looks like a repeating key! You can extract it using a python script or simply by looking at whats reapiting, in this case we can clearly see that `eDWo` is repeating, which is the key. Or use this script:

```python
def detect_repeating_key(key):
    for i in range(1, len(key)):
        if (key[:i] * (len(key) // i + 1))[:len(key)] == key:
            return key[:i]
    return key

print("Repeating XOR key:", detect_repeating_key(xor_key))
```

Output:
```
b'eDWo'
```

✅ **Our actual XOR key is:** `eDWo`



### 4. **Create a Cookie to Show the Password**

We’ll craft a new JSON object:
```json
{"showpassword":"yes","bgcolor":"#000000"}
```

Now XOR this with the key, then base64 encode it:

```python
import base64

def xor_encrypt(data, key):
    return bytes([ord(data[i]) ^ key[i % len(key)] for i in range(len(data))])

new_plaintext = '{"showpassword":"yes","bgcolor":"#000000"}'
key = b"eDWo"

# Encrypt
encrypted = xor_encrypt(new_plaintext, key)

# Encode
cookie_value = base64.b64encode(encrypted).decode()
print("🔐 New Cookie Value:", cookie_value)
```

Take the value of `cookie_value` and paste it in your browser's cookie storage under:
```
Storage → Cookies → data
```

**Reload the page**, and if everything worked:
- ✅ The background color will change to black
- ✅ The password will be revealed



### 📁 If you're stuck

I've written a `decode.py` script to automate this entire process. It helps reinforce each of the steps and makes experimenting easier.




