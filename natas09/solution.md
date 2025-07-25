# 🔐 Natas 9 Walkthrough

We are given a search tab `Find words containing:` and again there is a [View sourcecode](http://natas9.natas.labs.overthewire.org/index-source.html) link. By following with the link we can see a `PHP` script:

```php
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    passthru("grep -i $key dictionary.txt");
}
?>
```

This script uses the `grep` command, which searches for lines in a file that match a specified pattern or keyword. The important detail here is that user input `($_REQUEST["needle"])` is passed ***unprotected*** into a shell command via `passthru()` — opening the door for command injection.

## :question: How Do We Exploit This?

The PHP code runs a command like this:

```bash
grep -i $input dictionary.txt
```
If we enter a specially crafted input, we can inject additional shell commands. This allows us to execute arbitrary commands on the server. Our goal is to read the contents of the file `/etc/natas_webpass/natas10`, which stores the password for the next level.


## 🧪 The Exploit
We can use the `cat` command to read the  `/etc/natas_webpass/natas10` file :

```bash
grep -i something; cat /etc/natas_webpass/natas10 
```

Lets explain this code:

1. `something;` 
    - This ends the `grep` command early.
    - The semicolon `;` tells the shell: ***"I'm done with the first command, start a new one."***

2. `cat /etc/natas_webpass/natas10`
    - This command prints the contents of the file containing the password for natas10. 


After successfully injecting the command, the server will execute `cat /etc/natas_webpass/natas10` and return the password for the next level.


