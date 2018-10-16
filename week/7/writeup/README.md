Writeup 7 - Forensics I
======

Name: Justin Van Dort
Section: 0102

I pledge on my honor that I have not given or received any unauthorized assistance on this assignment or examination.

Digital acknowledgement of honor pledge: Justin Van Dort

## Assignment 7 writeup

### Part 1 (40 pts)

1. PNG

    ```
    $ binwalk image

    DECIMAL         HEX             DESCRIPTION
    ---------------------------------------------------------------------------------------------
    12              0xC             TIFF image data, big-endian
    2395936         0x248F20        PNG image, 960 x 720, 8-bit/color RGBA, non-interlaced
    ```

2. Using `exiftool`, I was able to extract the GPS data from the image's EXIF data. 

    The GPS position was `41 deg 53' 54.87" N, 87 deg 37' 22.53" W`. With `https://www.fcc.gov/media/radio/dms-decimal`, I was able to convert this to a decimal GPS coordinate and discover that the image was taken at the `John Hancock Center in Chicago, IL`.

3. The timestamp in the EXIF data was `2018:08:22 11:33:24.801`.

4. This photo was taken by an `Apply iPhone 8`. 

5. The GPS altitude from the EXIF data was `539.5 m Above Sea Level`.

6. `CMSC389R-{look_I_f0und_a_str1ng}`

    ```
    $ strings image | grep CMSC

    You found the hidden message! CMSC389R-{look_I_f0und_a_str1ng}
    ```

### Part 2 (55 pts)

The first thing I did with the binary was run `binwalk`.

``` 
$ binwalk binary

DECIMAL         HEX             DESCRIPTION
-------------------------------------------------------------------------------------------------
0               0x0             ELF 64-bit LSB shared object, AMD x86-64, version 1 (SYSV)
1131            0x46B           LZMA compressed data, properties: 0x09, dictionary size: 131072 bytes, uncompressed size: 69 bytes
16656           0x4110          LZMA compressed data, properties: 0x1B, dictionary size: 16777216 bytes, uncompressed size: 33554432 bytes
17360           0x43D0          LZMA compressed data, properties: 0x89, dictionary size: 16777216 bytes, uncompressed size: 100663296 bytes
17552           0x4490          LZMA compressed data, properties: 0xA3, dictionary size: 16777216 bytes, uncompressed size: 100663296 bytes
17744           0x4550          LZMA compressed data, properties: 0xBF, dictionary size: 16777216 bytes, uncompressed size: 33554432 bytes
```
After discovering that the binary contained executable code, I ran it (It may not have been the best idea to run some "random" code I found on the internet). 

```
$ ./binary

Where is your flag? 
```
I also tried extracting the 'LZMA' compressed data with 7zip, but I could not get the file to extract. So, I decided to analyze the binary with `objdump`.

```
$ objdump -d binary

...

0000000000000784 <main>:
 784:   55                      push   %rbp
 785:   48 89 e5                mov    %rsp,%rbp
 788:   48 83 ec 20             sub    $0x20,%rsp
 78c:   c6 45 ec 2f             movb   $0x2f,-0x14(%rbp)
 790:   c6 45 ed 74             movb   $0x74,-0x13(%rbp)
 794:   c6 45 ee 6d             movb   $0x6d,-0x12(%rbp)
 798:   c6 45 ef 70             movb   $0x70,-0x11(%rbp)
 79c:   c6 45 f0 2f             movb   $0x2f,-0x10(%rbp)
 7a0:   c6 45 f1 2e             movb   $0x2e,-0xf(%rbp)
 7a4:   c6 45 f2 73             movb   $0x73,-0xe(%rbp)
 7a8:   c6 45 f3 74             movb   $0x74,-0xd(%rbp)
 7ac:   c6 45 f4 65             movb   $0x65,-0xc(%rbp)
 7b0:   c6 45 f5 67             movb   $0x67,-0xb(%rbp)
 7b4:   c6 45 f6 6f             movb   $0x6f,-0xa(%rbp)
 7b8:   c6 45 f7 00             movb   $0x0,-0x9(%rbp)

...
```

The program appeared to be creating a string on the stack, so I decoded the ASCII values to `/tmp/.stego`. The binary was creating a file in the `tmp` directory, presumably by extracting the data within its own file. 

The first step is to run `binwalk`. 

```
$ binwalk

DECIMAL         HEX             DESCRIPTION
-------------------------------------------------------------------------------------------------------
```

That's no help. `strings` didn't reveal anything interesting either. So, the next step is to open the file in a hex editor to see if I can manually figure out the file type. The first thing I noticed was `JFIF` written near the beginning of the file. Wikipedia's list of file signatures led me to JPEG file signature of `FF D8 FF E0 00 10 4A 46 49 46 00 01`. `stego` started similarly, but had a leading `00`. After deleting the first byte, I was able to rename the file to `stego.jpg` and open it with an image viewer. 

My next thought was to look for steganographic data hidden in the image. 

```
$ steghide extract -sf stego.jpg -xf out.txt

Enter passphrase:
Premature end of JPEG file
steghide: could not extract any data with that passphrase!
```

Passphrase? Premature end of file? Well, it turns out all jpg files end in `FF D9`, but `stego` only ended in `FF`. Adding `D9` in a hex editor stopped the error message from appearing. 

The final step is to actually extract the data from the image. I found a bash script online to bruteforce `steghide` with a wordlist, and ran it with `rockyou.txt`. After some time of running the script, I decided not the pursue this approach.

At this point, I was stuck and posted a question on piazza. The answer stated that the image would be `bruteforcable via rockyou.txt`, and that I chould `think about what clues ... [I've] already found`. 

At this point, I knew I had come across the password at some point, so I just needed to look. I searched for `stego` in `rockyou.txt` and found `stegosaurus`. 

```
$ steghide extract -sf stego.jpg -xf out.txt -p stegosaurus

wrote extracted data to "out.txt".

$ cat out.txt

Congrats! Your flag is: CMSC389R-{dropping_files_is_fun}

```

The file contained the flag: `CMSC389R-{dropping_files_is_fun}`