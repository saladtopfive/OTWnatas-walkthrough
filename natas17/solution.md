
# 🔐 Natas17 Walkthrough

This level is very similar to **natas15**, especially if we look at the [source code](http://natas17.natas.labs.overthewire.org/index-source.html). We can see almost identical logic, with the main difference being **output handling**:

```php
if(mysqli_num_rows($res) > 0) {
    //echo "This user exists.<br>";
} else {
    //echo "This user doesn't exist.<br>";
}
} else {
    //echo "Error in query.<br>";
}
```

As you can see, all `echo` statements are commented out. This means that nothing is displayed in the server response.  

In practice, this means we cannot use the `natas15/16` script, which relied on analyzing `response.text()`. We need to come up with **another way to extract the password for natas18**, for example by using a time-based attack (`sleep`) instead of checking the response content.

## :clock1: Time-Based Attack

Since the server does not return any output that indicates whether a query was successful or not, we cannot rely on checking the page content to extract the password.  

A **time-based attack** exploits the fact that the database can be instructed to delay its response under certain conditions. For example, using MySQL's `IF()` function together with `sleep()`:

```sql
IF(condition, SLEEP(2), 0)
```

- `condition` is an expression that evaluates to `TRUE` or `FALSE`.  
- If the condition is true, the server will pause for 2 seconds before responding.  
- If the condition is false, it responds immediately.

By measuring how long the server takes to respond, we can infer whether our condition was true. In the context of Natas17, we can check one character at a time of the password:

```sql
IF(BINARY substring(password,1,1) = 'a', SLEEP(2), 0)
```

- If the first character of the password is `'a'`, the server waits 2 seconds.  
- Otherwise, it responds immediately.  

By iterating over all possible characters and positions, we can gradually reconstruct the full password. This method is especially useful when there is no visible output to analyze.


