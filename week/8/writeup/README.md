Writeup 8 - Forensics II, Network Analysis and File Carving/Parsing
=====

Name: Justin Van Dort
Section: 0102

I pledge on my honor that I have not given or received anyunauthorized assistance on this assignment or examination.

Digital acknowledgement of honor pledge: Justin Van Dort

## Assignment 8 Writeup

### Part 1 (45 Pts)

Wireshark was very helpful in reading the `pcap` file. For example, to view all communications between the hackers: 

    (ip.addr == 104.248.224.85 or ip.addr == 206.189.113.189)  and tcp.len > 0

And to view traceroute

    udp or icmp

1. The `pcap` file showed evidence of a traceroute to `128.8.120.43` and to `216.58.219.238`. Typing these IP addresses into a web browsers showed that they belon to The UMD Cybersecurity Club and Google, respectively. See packet numbers 142-153 and 506-517. 

2. The hackers used the names `laz0rh4x` and `c0uchpot4doz`.

3. 

Name | IP | Location
--- | --- | ---
laz0rh4x 	    | 104.248.224.85  | DigitalOcean, US, NYC
c0uchpot4doz	| 206.189.113.189 | DigitalOcean, UK, London

4. The hackers used port 2749 on the server. 

5. The full transcript of the communications: 

```
134 laz0rh4x -> c0uchpot4doz : hey man, are you there?  
229 c0uchpot4doz -> laz0rh4x : yeah. when is it happening?  
258 laz0rh4x -> c0uchpot4doz : we're all set for tomorrow at 1500  
474 laz0rh4x -> c0uchpot4doz : did you get the updated plans?  
490 c0uchpot4doz -> laz0rh4x : no, can you send them over?  
498 laz0rh4x -> c0uchpot4doz : https://drive.google.com/file/d/1McOX5WjeVHNLyTBNXqbOde7l8SAQ3DoI/view?usp=sharing  
612 laz0rh4x -> c0uchpot4doz : done. you can read that with the parser I gave you last week  
616 c0uchpot4doz -> laz0rh4x : thanks, see you tomorrow  
676 laz0rh4x -> c0uchpot4doz : good luck, don't be late  
```
They plan to do something "tomorrow" at 3:00 PM (today being Oct 24th). The plans are contained within a file on google drive. 

6. https://drive.google.com/file/d/1McOX5WjeVHNLyTBNXqbOde7l8SAQ3DoI/view?usp=sharing 

7. They plan to see eachother "tomorrow", October 25th at 3:00 PM.

### Part 2 (55 Pts)

*Report your answers to the questions about parsing update.fpff below.*
1. The timestamp of `update.fpff` is `2018-10-25 00:40:07`. 

2. The author of `update.fpff` is `laz0rh4x`. 

3. The file claims to have `9` section, but actually has `11`. 

4.

```
------- HEADER -------
MAGIC: 0xdeadbeef
VERSION: 1
TIMESTAMP: 2018-10-25 00:40:07
AUTHOR: laz0rh4x
SECTION COUNT: 9
```
```
-------  BODY  -------
SECTION 0, TYPE: ASCII, LENGTH: 51
Call this number to get your flag: (422) 537 - 7946

SECTION 1, TYPE: WORD ARRAY, LENGTH: 60
[3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9]

SECTION 2, TYPE: LAT-LNG, LENGTH: 16
(38.99161, -77.02754)

SECTION 3, TYPE: REFERENCE, LENGTH: 4
Section Number: 1

SECTION 4, TYPE: ASCII, LENGTH: 60
The imfamous security pr0s at CMSC389R will never find this!

SECTION 5, TYPE: ASCII, LENGTH: 991
The first recorded uses of steganography Can be traced back to 440 BC when Herodotus Mentions two exampleS in his Histories.[3] Histicaeus s3nt a message to his vassal, Arist8goras, by sha9ving the hRead of his most trusted servan-t, "marking" the message onto his scal{p, then sending him on his way once his hair had rePrown, withl the inastructIon, "WheN thou art come to Miletus, bid _Aristagoras shave thy head, and look thereon." Additionally, demaratus sent a warning about a forthcoming attack to Greece by wrIting it dirfectly on the wooden backing oF a wax tablet before applying i_ts beeswax surFace. Wax tablets were in common use then as reusabLe writing surfAces, sometimes used for shorthand. In his work Polygraphiae Johannes Trithemius developed his so-called "Ave-Maria-Cipher" that can hide information in a Latin praise of God. "Auctor Sapientissimus Conseruans Angelica Deferat Nobis Charitas Gotentissimi Creatoris" for example contains the concealed word VICIPEDIA.[4}

SECTION 6, TYPE: LAT-LNG, LENGTH: 16
(38.9910941, -76.9328019)

SECTION 7, TYPE: PNG, LENGTH: 245614
 > See extracted7.png

SECTION 8, TYPE: ASCII, LENGTH: 22
AF(saSAdf1AD)Snz**asd1

SECTION 9, TYPE: ASCII, LENGTH: 45
Q01TQzM4OVIte2gxZGQzbi1zM2N0MTBuLTFuLWYxbDN9

SECTION 10, TYPE: DWORD ARRAY, LENGTH: 48
[4, 8, 15, 16, 23, 42]
```

5. 

run `test.py` on section 5: `CMSc389R-{PlaIN_dIfF_FLAG}`  
Base64 decode Section 9:    `CMSC389R-{h1dd3n-s3ct10n-1n-f1l3}`  
flag in section 7 image:    `CMSC389R-{c0rn3rst0ne_airlin3s_to_the_moon}`

At first, for the plan diff flag, I saw curly braces in the section 5 text, so I figured there was a flag hidden there. Then I noticed how some letters were capitalized when they shouldn't be, so I started by deleting and lowercase letters (and spaces and quotes). But that just gave me gibberish. I googled the beginning portion of the text and found it in wikipedia. So, then I wrote a short python script to find the differences and the output was the flag above. 

I also called the number in the first section, but the phone number seemed to be inactive. 