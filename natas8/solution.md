# 🔐 Natas 8 Walkthrough

Again we face an input window and a ***View sourcecode*** link. So naturally we check 
it out. This takes us to the ***php*** script which we need to understand. The first 
thing that should catch our eyes is the variable named:

```php
$encodedSecret = "3d3d516343746d4d6d6c315669563362";
```

This gives us the clue that the password or the ***secret*** is encoded. To understand
how its encoded we just need to look a few lines below the variable definition:

```php
function encodeSecret($secret) {
    return bin2hex(strrev(base64_encode($secret)));
}
```


This function clearly takes the ***secret*** through 3 steps, which are:

- bin2hex - Converts a binary string (raw text) into a hexidecimal representation.
- strrev - Reverses the string.
- base64 - Encodes binary or text data into a base64 format, which is a way to represent binary data using ASCII characters.


## 🔍 How to crack this password?

So in order to get the original password, we need to go on the reverse order of these
actions. To do that we can use many different tools. I recommend we use:

- The bash terminal (for reversing the string and decoding base64)
- [CyberChef](https://gchq.github.io/CyberChef/) (a github project hosted on a github.io server for reversing bin2hex)

## ❗ The steps to take 

1. Get the encoded password `$encodedSecret = "3d3d516343746d4d6d6c315669563362";`
2. Paste the string into the CyberChef ***From Hex*** tab, this gives us the raw text back.
Now `==QcCtmMml1ViV3b`
3. Paste the converted back raw text to your bash and run a reversestring command such as: 

```bash
echo ==QcCtmMml1ViV3b | rev
```

4. Paste the converted+reversed data into your bash again and run a base64 decode command:

```bash
echo b3ViV1lmMmtCcQ== | base64 --decode
```
5. That will give you the ***secret***. Which you need to input in the main website. 

## :boom: Alternitevly

I made a python script called `decoder-script.py` where you can just paste the encoded secret.

```python
import base64

print('enter the encoded secret:')
secret = input()
secret = bytes.fromhex(secret)
secret = secret[::-1]
secret = base64.decodebytes(secret)

print("Decoded secret:", secret.decode('utf-8', errors='replace'))
```

By following these steps will grant you access into natas9.


