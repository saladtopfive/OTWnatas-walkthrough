# 🔐 Natas14 Walkthrough

Here we have a login window. This suggests to us that sql injection will be used here.

## What is sql injection?
Sql injection is a technique to enter a database. Basic sql injection technique's use `"` as their **weapon.** Let's take a look at an example:

```
SELECT * from databaseTableOfUsers where username = "$userProvidedUsername" and password = "$userProvidedPassword"
```

We can use `"` in our password and username inputs to our advantage. For example:

Input:
```
username = something
password = lol" or "1
```
How it will look in the script once we input it:
```
SELECT * from databaseTableOfUsers where username = "something" and password = "lol" or "1"
```
As you can see the password checking logic now has an ***always true value*** `1` = always true. So the password will be given to us.
As always, let's check whats under the [View sourcecode](http://natas14.natas.labs.overthewire.org/index-source.html) link. And look for a vunerability like that in the code.
From the sourcecode we can deduct that the `php` script look for usernames and passwords in a database:

```php
$link = mysqli_connect('localhost', 'natas14', '<censored>');
    mysqli_select_db($link, 'natas14');
```

The next line is what interests us:

```php
$query = "SELECT * from users where username=\"".$_REQUEST["username"]."\" and password=\"".$_REQUEST["password"]."\"";
```
It look exactly like that previous example. The backticks can look complicated but its actually exactly the same code!
