# 🔐  Natas 6 Walkthrough

This website contains an input window, it tells us to input a ***secret.*** On the right
bottom of the input window we can see a [View SourceCode](http://natas6.natas.labs.overthewire.org/index-source.html)
Naturally we click it. 

## 🧠  Introduction

This introduces us to PHP scripting. PHP is a backend scripting
language we can see that its being used here for the login logic. Its usually implemented
with `<? ?>` or `<?php ?>`.

```
<?
include "includes/secret.inc";

    if(array_key_exists("submit", $_POST)) {
        if($secret == $_POST['secret']) {
        print "Access granted. The password for natas7 is <censored>";
    } else {
        print "Wrong secret";
    }
    }
?>
```

Reading this code we can see that it checks if a variable `$_POST` matches the ***'secret'***
what exactly is the ***'secret'***? Lets focus on the first line: `include "includes/secret.inc";`
This line tells us that there is a file that contains the password (secret) that we need 
to find. Simply add this `/includes/secret.inc` to the end of the url. Like so:

```http://natas6.natas.labs.overthewire.org/includes/secret.inc```

This will direct you to a seemingly open site, but you can see that it exactly that. It 
connected you to this seemingly open site. Which means there has to be something happening,
no errors, nothing. We inspect the site and in the header we can find: 

> [!NOTE]
> $secret = 'AAAAAAAAAAAAAAAA' (depending on your playthrough)

Paste in that phrase and you will be granted access to natas7.



