Writeup 3 - Pentesting I
======

Name: Justin Van Dort
Section: 0201

I pledge on my honor that I have not given or received any unauthorized assistance on this assignment or examination.

Digital acknowledgement of honor pledge: Justin Van Dort

## Assignment 4 Writeup

### Part 1 (45 pts)
After running `nc cornerstoneairlines.co 45`, I was greeted with a prompt to enter an IP address. Since I knew the ping service used the linux ping command, and since I knew the service was vulnerable to command injection, the first thing I entered was `; ls`. The response was `bin boot dev etc home lib lib64 media mnt opt proc root run sbin srv sys tmp usr var`, and I knew I found the injection vulnerability.

By entering `; ls`, I was assuming that the input from the IP prompt was being simply concatinated to an existing command and run in the shell. The semicolon discards the previous command, so everything to the right of the semicolon will be run in the shell as if there was no text before it. Finding the flag was as simple navigating to the `home` directory and finding `flag.txt`. The flag is: `CMSC389R-{p1ng_as_a_$erv1c3}`. The script which ran the ping service is `/opt/container_startup.sh`. I found this by redirecting stderr to stdout. Then, if I ran a command that did't exist, I recieved `/opt/container_startup.sh: line 29:`, followed by the error. 

In terms of vulnerabilities, Fred could have avoided this attack by sanitizing the input to the shell script which hosted the ping service. The sanitization scheme couuld be verifying that the input string matches a regex of an IP address or hostname. At the very least, Fred could have made sure to run the script as an unprivileged user so that a different vulnerability would only lead to unprivileged access to the machine. Lastly, Fred could have written a separate program which took the input string (perhaps in C), which directly performed the ping operation, so that the service would not be vulnerable to command injection through the shell. 

### Part 2 (55 pts)

After finding the vulnerability, making an interactive shell was relatively straightforward. In essence, for each command, the shell strips the initial header that the server sends, and sends the input command preceeded by a semicolon. One issue with this approach is that all commands ran in this fashion are ran within the root directory. 

By wrapping the command like so: `(cd <path>; <command>)`, each command will be ran from the desired path. I intercept each cd command and simply change the local `path` variable instead of sending the command to the server. Then with the `is_directory` function I wrote, I could determine if the desired path is valid. 

The final command sent to the server is: `;(cd <path>; <command>) 0<&- 2>&1`. `0<&-` closes stdin so that commands like `bash` do not run indefinitely. `2>&1` redirects stderr to stdout so that errors can be seen in this shell. 

`pull` is implemented by `cat`ing the desired file on the remote side, and saving the resulting data to a file. I also made a `is_file` function to determine if the remote file exists. 

Usage:

run `./hack.py` or `python3 hack.py`. This script was written for python3. 

After running the program, type `shell` for shell access to the server, and `exit` to exit the shell access. `pull <remote file> <local file>` fill transfer a remote file to the local machine. `help` shows a menu of all commands, and `quit` exits `hack.py`.