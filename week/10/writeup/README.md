Writeup 10 - Crypto II
=====

Name: Justin Van Dort
Section: 0102

I pledge on my honor that I have not given or received anyunauthorized assistance on this assignment or examination.

Digital acknowledgement of honor pledge: Justin Van Dort

## Assignment 10 Writeup

### Part 1 (70 Pts)

For the most part, part 1 of homework 10 was relatively straightforward. The general structure of the code is as follows:

```
1) Generate md5(secret + message + padding) via server
2) Generate md5(secret + message + padding + malicious) locally by initializing md5 state with output from above
3) For each possible secret length (6 to 15 bytes), do the following:
4) Calculate the proper padding based on guessed secret size and message
5) Send message + padding + malicious, so that server will calculate md5(secret + message + padding + malicious)
6) If fake_hash is equal to the server's generated hash, then the correct secret length has been found. 
```

I wrote a script to perform these tasks. See `stub.py`. Running the script results in the following output (output will change based on generated secret, but the structure remains the same). The last line of the script's output is the flag. 

```
Message: CMSC389R Rocks!
Malicious: 1
Hash is "92db9ee81e735c5aa9f230191fa34043"
Fake hash is "01037d172ae701bcc8ae6439d633a149"
Payload: CMSC389R Rocks!\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xc8\x00\x00\x00\x00\x00\x00\x001
CMSC389R-{i_still_put_the_M_between_the_DV}
```

The flag: **CMSC389R-{i_still_put_the_M_between_the_DV}**

For some reason, the server will return unexpected output and the program will crash. But, running the script again will produce the correct output. 

The most difficult problem I faced was not getting the flag from the server, even after calculating the padding and payload. After a bunch of troubleshooting and printing out intermediatery values, I realized that I wasn't including the size of the secret in the message length field in the padding. After making the correction, the program worked properly. 



### Part 2 (30 Pts)

generating keys  
```
gpg --gen-key
> Follow instructions (Enter Name, Email, Passphrase)
```
importing someone else's public key  
```
gpg --import <public.key>
```
encrypting a message for that someone else and dumping it to a file  
```
gpg -e -r <email> -o <output file> <message file>
```
