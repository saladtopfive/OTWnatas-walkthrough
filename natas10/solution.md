# 🔐 Natas 10 Walkthrough


The setup is very similar to Natas 9, but this time some characters are filtered to make command injection harder. By viewing the  [sourcecode](http://natas10.natas.labs.overthewire.org/index-source.html), we can see exactly what’s being blocked:

 ```php
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    if(preg_match('/[;|&]/',$key)) {
        print "Input contains an illegal character!";
    } else {
        passthru("grep -i $key dictionary.txt");
    }
}
?>
 ```
## 🔍 What's different?
As we can see, the characters `;`, `|`, and `&` are filtered.

***But we don't actually need them.***

The trick is to realize that `grep` is capable of searching through **multiple files** at once. We don't have to break out of the `grep` command at all — instead, we can **abuse the fact that `grep` will read and display any file we tell it to**, as long as we provide a valid search pattern.

Since the filter only blocks breaking out of `grep`, our approach will be to stay inside `grep`, but give it the file we want to read — such as `/etc/natas_webpass/natas11`. Let's try it then:

```bash
grep -i . /etc/natas_webpass/natas11 dictionary.txt
```

## 💡 Why `.`? 
 Because in regular expressions, `.` is a wildcard that matches **any single character**. This ensures that `grep` will print any non-empty line — like the one containing the password.


## 🧪 Final Input
To trigger that exact command on the server, simply input this into the search field:
```
. /etc/natas_webpass/natas11
```
The password should appear at the top of the output.