# Natas3 Walkthrough

Okay, this is a weird one if you've never heard of it before. So here's a little bit of
insight: 

There are so-called **web crawlers** all over the internet. They're basically bots that
browse the web to build indexes of it. So that when you search something like:

> "femboy feet" 😳

...the search engine knows **exactly** which sites will suit you best.

---

### 🕵️ Step 1: Inspect the Page

When inspecting the page source of Natas3, we find this little comment:

```html
<!-- No more information leaks!! Not even Google will find it this time... -->
```

its indicating that we should look for robots.txt, a file placed at the root of a website
that tells web crawlers which parts of the site they should/shouldnt index. So naturally
we go to that file. By adding /robots.txt at the end of the url:

```
http://natas3.natas.labs.overthewire.org/robots.txt
```

Following this link we can see some text that states:

> User-agent: *
> Disallow: /s3cr3t/

This is basically talling the crawlers to not go to /s3cr3t/. Thats exactly where we will
go.

```
http://natas3.natas.labs.overthewire.org/s3cr3t/
```
There we can see again, users.txt, after opening it we see that it contains the password
for natas4.


