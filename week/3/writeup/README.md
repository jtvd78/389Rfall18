Writeup 3 - OSINT II, OpSec and RE
======

Name: Justin Van Dort
Section: 0201  

I pledge on my honor that I have not given or received any unauthorized assistance on this assignment or examination.

Digital acknowledgement of honor pledge: Justin Van Dort

## Assignment 3 Writeup

### Part 1 (100 pts)

Vulnerabilities:
1) No protection against port scans or bruteforce dictionary attacks 
2) Shell access directly accessble via open port
3) No key-based authentication

#### No protection against port scans or bruteforce dictionary attacks 

A significant vulnerability with Fred's admin server was the lack of any
intrusion detection or prevention systems. Without IDS/IPS, attackers can 
perform a port scan on the target to help determine which services are being 
hosted on the server. Furthermore, without IDS, an attacker would be able to 
bruteforce password attempts (like in week 2 HW) to gain access to the system. 

Tools like Fail2Ban and Snort are able to analyze log files in real time and
detect specific traffic patterns which may indicate suspicious network activity 
on the server. After discovering a malicious IP address, these IDS tools usually
block the address via a firewall rule. If Fred has used an IDS/IPS system on his
admin server, the week 2 attack would not have been possible. 

#### Shell access directly accessble via open port, without encryption

Fred's admin server was hosting a text-based shell service on port 1337. The
login prompt was a simple shell script, and provided no encrpytion. This is vulnerable
to a man-in-the-middle attack since Fred's connection to the server is unencrypted. But, 
even if Fred used SSH (which he should), an attacker would still be able to bruteforce 
the password prompt for SSH. 

In order to further hide the shell access, Fred could implement port knocking to help
hide the availability of his SSH server. Port knocking hides the existence of an open port
(and the service behind it) by requiring the user to first attempt to connect to a certain set
of ports in a certain order. Only then would the user be abele to connect to the hidden port. 
To close the hidden port, the user would usually 'knock' on each port in the reverse order. 
If Fred had used SSH and port knocking, his shell access to the server would have been 
both encrypted and hidden from attackers. 

#### No key-based authentication

Finally, Fred's shell service was authenticated via a password, which makes dictionary
attacks possible. Had Fred not used the above two methods to protect his server, he could have
implemented his shell authentication via public/private key pairs (usually via SSH). Using key authentication, bruteforcing the password to log into the shell access would not be possible. 

In addition to not using a key for authentication, the shell that was hosted by the server was
ran by the root user. A better alternative would be to disable login for the root user and 
create an admin use with sudo permissions. Since sudo can be logged, it is possible to record
the commands that a malicious users entered, in order to determine any damage caused to the 
system, or to perform security audits. 

#### Additional Vulnerabilities:

* Link to admin server was accessable via webpage
* Git repository accessable via HTTP
* robots.txt revealed hidden directories
* Weak password for root login