# 🔐 Natas 5 Walkthrough

When logging in with natas5 and the provided password, we are shown the message: 

> [!TIP]
>***You're not logged in.*** 

Naturally, we inspect the browser's Developer Tools, and we notice that this website uses HTTP, a stateless protocol. This means the server doesn't maintain any persistent session information between requests. To manage user sessions, websites often rely on the browser to store session-related data in the form of cookies.

Cookies are stored on the client side (i.e., in the browser), and depending on how they're implemented, they can be stored as:

- Plain text, 
- hash or encrypted, 
- encoded (e.g., Base64). 

Which determines how hard it is to manipulate them. ***Luckily for us, they are stored in 
plain text on this site.***

## 🧠 How do we change authentication cookies?

Inspect the website and navigate to the ***storage -> cookies.*** Clicking the website link
in said tab you'll see the:

```loggedIn = 0```

Variable, simply change it to ***1***:

```loggednIn = 1``` 

Refreshing the site will grant you the password to natas6.
