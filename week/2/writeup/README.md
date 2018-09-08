Writeup 2 - OSINT (Open Source Intelligence)
======

Name:  Justin Van Dort  
Section: 0201  

I pledge on my honor that I have not given or received any unauthorized assistance on this assignment or examination.

Digital acknowledgement of honor pledge: Justin Van Dort  

## Assignment 2 writeup

### Part 1 (45 pts)

1. What is `kruegster1990`'s real name?  
    I first started by checking for `kruegster1990` at `checkusernames.com`, and found his 
    Twitter account `@kruegster1990`. From there, I found his real name.   
    **Fred Krueger**

2. List all personal information (including social media accounts) you can find about him. For each, briefly detail how you discovered them.   
    | Info          | Source                | Value |     
    | ------------- |-------------          | -----
    | Twitter	    | checkusernames.com    | https://twitter.com/kruegster1990
    | Instagram	    | knowem.com            | https://www.instagram.com/kruegster1990/
    | Reddit		| checkusernames.com    | https://www.reddit.com/user/kruegster1990
    | Website       | Twitter               | http://www.cornerstoneairlines.co/
    | Email		    | Cornerstone Airlines Website  | kruegster1990@tutanota.com  
    | Location      | Twitter               | Silver Spring, MD
    | Previous Flight | Instagram           | Flight AAC27670

3. What is the IP address of the webserver hosting his company's site? How did you discover this?  
    * `142.93.118.186` is the IP of the website (cornerstoneairlines.co) 
        * Discovered via `ping cornerstoneairlines.co`    
    * `142.93.117.193` is the IP address of the admin page (There is no domain name)

4. List any hidden files or directories you found on this website. Did you find any flags?  
    I did not find any hidden subdirectories until I read this question. I opened robots.txt to find
	a secret directory, http://www.cornerstoneairlines.co/secret/  
	Found flag: **CMSC389R-{fly_th3_sk1es_w1th_u5}**

    I wanted to find more directories, so I ran:  
    `dirb http://142.93.118.186/`, which found the `.git` directory.  

    Then I ran `wget -r -F -v cornerstoneairlines.co/.git/` to get the files.  
    After looking through the repository, I found **CMSC389R-{y0u_found_th3_g1t_repo}**  
    Fred was committing with the email, `kruegster@tutanota.com`.
    This led me to a search for accounts online with this username (`kruegster`), 
    but all the results I found were for other people. 

5. Did you find any other IP addresses associated with this website? What do they link to, or where did you find them?

    * `142.93.117.193` is the IP address of the admin page.  
        * Found by looking at the address bar in chrome when visiting the admin page. 
    * Git repo has no remote.  
    * `/opt/container_startup.sh` seemed to be sending all commands to `129.2.94.135` 
        at port `3321`, through the IP does not seem to be active. 

6. If you found any associated server(s), where are they located? How did you discover this?
    
    * `142.93.118.186` (cornerstoneairlines.co) is a DigitalOcean server, in New York NY
        * Via `https://tools.keycdn.com/geo?host=142.93.118.186`
    * `142.93.117.193` (admin server) is a DigitalOcean server, in New York NY
        * Via `https://tools.keycdn.com/geo?host=142.93.117.193`

7. Which operating system is running on the associated server(s)? How did you discover this?

    Ubuntu

    ```
    $ nc 142.93.118.186 80
    > <Enter>
    > ...
    > Server: Apache/2.4.18 (Ubuntu)

    $ nc 142.93.117.193 80
    > <Enter>
    > ...
    > Server: Apache/2.4.18 (Ubuntu)
    ```



8. **BONUS:** Did you find any other flags on your OSINT mission? (Up to 9 pts!)

    * Found flag in source of http://www.cornerstoneairlines.co/
        * **CMSC389R-{h1dden_fl4g_in_s0urce}**  
    * Using "discover" domain search in DNS record
        * **CMSC389R-{dns-txt-rec0rd-ftw}**
    * Using bruteforce to find flight record
        * `142.93.117.193` (admin server) on port `1337`
        * Username: `kruegster` (username found from git repo email)
        * Password: `pokemon` (brute force)
        * Flight number: `AAC27670` (From Instagram)
        * Path to flight records `/home/flight_records` (via `ls` and `cd`)
        *  **CMSC389R-{c0rn3rstone-air-27670}**

### Part 2 (55 pts)

I started by looking up `kruegster1990` on `checkusernames.com`, and found his Twitter and Reddit accounts.
After searching with other username lookup websites, I found his Instagram account. 

Looking through his Instagram account, he seemed obsessed with pokemon, but he also had a plane
ticket posted to his account. Noted. His twitter account revealed his full name, and had a link to 
his comapny's website, cornerstoneairlines.co. I opened the link and searched each page until I found
the admin page, which seemed like the best target to _hack_. 

After finding the admin page, I knew I was at the right place. Now I had to gain access to the machine.
Finding `<!-- Keep looking, class! You're very close :) -->` in the source kept me reassured that 
the solution was close. 

First, I wanted to discover which services were running on the admin server.

```
$ nmap 142.93.117.193

> ...
> 80/tcp    open        http
> 514/tcp   filtered    shell
> 2222/tcp  open        EtherNetIP-1
> 10010/tcp open        rxapi
> 32755/tcp filtered    sometimes-rpc13
> ...
```

At the time of initial hacking, (as far as I remember) ports 514 and 32755 were not on this list. 
Port 80 was the web server, 2222 is for SSH (I cant hack that!), which leaves port 10010. Looking
up rxapi online brought up some dead software project, and `nc-ing` the port did nothing notable.  
  
Buy maybe the hidden service was being hosted on a nonstandard port?

```
$ nmap -p1-65535 142.93.117.193

> ...
> 1337/tcp  open        waste
> ...
```

This is promising.  
  
```
$ nc 142.93.117.193 1337
> Username: 
```

This is what I needed. I opened up the `stub.py` and made some modifications to make it 
work for the login prompt. Though, after running my script for some time with the usernames 
`kruegster1990` and `fred` there was no success. I also tried to make the script multithreaded, but failed 
with thread synchronization. 

Back to the drawing board, I wanted to see if I could find any other secret directories on the
airline page. `dirb http://142.93.118.186/` found a `.git` directory, which revealed a flag and 
the email `kruegster@tutanota.com`.
  
Re-running the script with username `kruegster` was successful, and gave me root "shell access" to the 
"machine". By "shell access" I mean stdout, but not stderr, and by "machine" I mean a docker container
with a read-only filesystem. 

The final flag **CMSC389R-{c0rn3rstone-air-27670}** was found by manually looking for the flight
records, which were conveniently located in `/home`. 

I tried to futher find more flags in the filesystem, but was restricted with the commands I could write. 
I looked for open ports, apache, nginx, to find the webserver or whatever was hosting on port 10010.
Typing `ufw`, `iptables`, `netstat`, `lsof`, etc. all produced no results, so with some quick googling, 
I discovered how to redirect stderr to std out. Each command I tried went from `<command>` to `<command> 2>&1`.
Turns out none of these commands were installed, and I could not install them since the filesystem
was read-only.

I attempted to find some kind of remote-code execution vulnerability. I could not create a file, so
I can't really call make on a C file. Python and PHP weren't installed, but Perl was. 

```
$ bash
perl <<< "print('hello');"
> hello
```

That's good enough for me. 