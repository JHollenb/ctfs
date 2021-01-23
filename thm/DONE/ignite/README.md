```
nmap -sC -sV $IP

PORT   STATE SERVICE VERSION
53/tcp open  domain?
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 1 disallowed entry
|_/fuel/
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Welcome to FUEL CMS

(base) jakeholl@Jakes-MacBook-Pro ignite % gobuster dir -u "http://$IP" -w common.txt -x php,txt,html
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.111.168
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Extensions:              php,txt,html
[+] Timeout:                 10s
===============================================================
2021/01/22 15:16:31 Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 292]
/.hta.php             (Status: 403) [Size: 296]
/.hta.txt             (Status: 403) [Size: 296]
/.hta.html            (Status: 403) [Size: 297]
/.htaccess            (Status: 403) [Size: 297]
/.htaccess.html       (Status: 403) [Size: 302]
/.htaccess.php        (Status: 403) [Size: 301]
/.htpasswd.php        (Status: 403) [Size: 301]
/.htpasswd            (Status: 403) [Size: 297]
/.htaccess.txt        (Status: 403) [Size: 301]
/.htpasswd.txt        (Status: 403) [Size: 301]
/.htpasswd.html       (Status: 403) [Size: 302]
/0                    (Status: 200) [Size: 16597]
/@.html               (Status: 400) [Size: 1134]
/@.php                (Status: 400) [Size: 1134]
/@.txt                (Status: 400) [Size: 1134]
/@                    (Status: 400) [Size: 1134]
/assets               (Status: 301) [Size: 315] [--> http://10.10.111.168/assets/]
/home                 (Status: 200) [Size: 16597]
/index                (Status: 200) [Size: 16597]
/index.php            (Status: 200) [Size: 16597]
/index.php            (Status: 200) [Size: 16597]
/lost+found           (Status: 400) [Size: 1134]
/lost+found.html      (Status: 400) [Size: 1134]
/lost+found.php       (Status: 400) [Size: 1134]
/lost+found.txt       (Status: 400) [Size: 1134]
/offline              (Status: 200) [Size: 70]
/robots.txt           (Status: 200) [Size: 30]
/robots.txt           (Status: 200) [Size: 30]
/server-status        (Status: 403) [Size: 301]
```

```
http://10.10.237.5/fuel/login/5a6e566c6243396b59584e6f596d3968636d513d
```
