# 🔐 Natas11 Walkthrough
On this level we are introduced to XOR encryption. Which is a reversible encryption process.. As long as you have the key that is. The easiest way to get a key for XOR encryption is to get your hand on a:
- Encrypted data,
- data befor encryption.

That way we can tell what the key is by comparing these two. Let's see what the [View sourcecode](http://natas11.natas.labs.overthewire.org/index-source.html) hides.


This is our xor ecnrypt function:
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

But looking below we can observe that the saveData function saves the TBC
