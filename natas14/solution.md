# 🔐 Natas14 Walkthrough

We’re presented with a login form. This hints that **SQL Injection** might be the intended path forward.

## 💡 What is SQL Injection?

SQL Injection is a technique used to manipulate a website’s database through its input fields. 

#### Example
Imagine a login system with a SQL query like this:

```php
SELECT * FROM users WHERE username = "$username" AND password = "$password";
```
Now suppose the attacker enters the following credentials:

```
username: admin 
password: password" OR "1 --
```

The query becomes:

```php
SELECT * FROM users WHERE username = "admin" AND password = "" OR 1=1 --";
```

Let's break it down:
- `""` closes the empty password string.
- `OR 1=1` always returns true.
- `--` comments out the rest of the query. (can be useful if you're not sure of the whole output but doesnt have to be used as you'll see in this level.)

So the final condition becomes:

```
username = "admin" AND (false) OR (true)
```
Which effectively bypasses the password check and logs in as `admin`.


## ✅ Exploit

Now, let’s check the source code for Natas14 at [View sourcecode](http://natas14.natas.labs.overthewire.org/index-source.html)

From the source, we see the following PHP code:
```php
$link = mysqli_connect('localhost', 'natas14', '<censored>');
mysqli_select_db($link, 'natas14');
```
Which indicates that the passwords and usernames are taken from a database.

Here’s the vulnerable part:
```php
$query = "SELECT * from users where username=\"".$_REQUEST["username"]."\" and password=\"".$_REQUEST["password"]."\"";
```
This is exactly the kind of vulnerable query we discussed earlier. It takes raw user input and inserts it directly into the SQL query without sanitization. That means **SQL Injection is possible**. Let's get rid of the `\` backticks so that the code is clearer:
```php 
SELECT * from databaseTableOfUsers where username = "$userProvidedUsername" and password = "$userProvidedPassword"
```
As you can see this is almost **exactly** our example.

Let's try the exact same credentials as in the example:

```
username: admin
password: lol" OR "1 
```

Resulting SQL query:
```php
SELECT * FROM users WHERE username="something" AND password="lol" OR "1";
```
The is a SQL comment operator, which means the rest of the query is ignored — effectively skipping the password check.

If successful, you’ll be logged in and shown the password for **Natas15**! :}
