# 🔐 Natas18 Walkthrough
In this level, we're asked to log in as an admin user. When we look at the [view sourcecode]() we quickly see that there isn't an sql injection vunerability like the previous levels. Instead, the vunerability lies in ***session management.***

## What is session management?
Http sites are stateless, meaning that each user gets their own session. Here we "simply" need to get access to the admin's session via ***PHPSESSID***. When we log in with arbitrary credentials, the site sets a ***PHPSESSID*** cookie. By experimenting, we can see that: 

- Each login attempt generates a numeric PHPSESSID stored in the storage tab in the developer tools.
- These IDs are assigned sequentially (1, 2, 3, ...).
- The application store wheter a session belong to `admin` or another user, **based solely on the PHPSESSID value.**

```php
function my_session_start() { /* {{{ */
    if(array_key_exists("PHPSESSID", $_COOKIE) and isValidID($_COOKIE["PHPSESSID"])) {
    if(!session_start()) {
        debug("Session start failed");
        return false;
    } else {
        debug("Session start ok");
        if(!array_key_exists("admin", $_SESSION)) {
        debug("Session was old: admin flag set");
        $_SESSION["admin"] = 0; // backwards compatible, secure
        }
        return true;
    }
    }

    return false;
}
```

This means we can brute-forfce possible PHPSESSID values until we find one that belongs to an **admin's** session.


