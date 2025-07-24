# 🔐 Natas2 Walkthrough

When inspecting this page you can find a message that states:
> "There is nothing on this page" 


Which is true but have a look at whats below:

```
<img src="files/pixel.png">
```

That line indicates that there is a folder called "files" on this website, so naturally we inspect. By going to:

```
http://natas2.natas.labs.overthewire.org/files/
```
We can see the contents of the folder, where we find users.txt. Clicking on it will grant us the credentials to ***natas3***.
