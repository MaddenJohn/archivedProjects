UTEID: jm76685;
FIRSTNAME: Jonathan;
LASTNAME: Madden;
CSACCOUNT: jm76685;
EMAIL: jm76685@cs.utexas.edu;

[Program 5]
[Description]
There is one java file: AES.java. This project takes in a file of hex text and uses the 256 bit key
Advanced Encryption Standard to encrypt text. This project also has the ability to decrypt a text using this same
256 bit key. The way this works is through a process of subBytes, mixColumns, shiftRows, and roundKey methods in 
a 14 round cycle to modify data. The key also is different for each round, which allows for a complex way of 
encrypting a file of data. This project also has error checking for input and times the throughput of both
the decrypting and encrypting process. The main method handles the calling of the encryption and decryption methods
which are then handled separately, calling the appropriate methods in the 14 round cycle. In subBytes a table is 
using for the sBox values to convert each value, in mixColumns I used the provided method by Bill Young, in shiftRows
I modified the strings accordingly to the algrithm, and lastly in the roundKey method I xor'd the data with a particular
key calculated from the initial key. On average, I found that the encryption process was faster than the decryption
process by looking at the throughput for each of the test cases.

[Finish]
I finished all of this project.

[Test Case 1]

[Command line]
java AES e key test1
java AES d key test1.enc

[Timing Information]
Encryption Throughput: 1600.0 Bytes in 85.0 ms  = 18.38235294117647 MB/Sec 
Decryption Throughput: 1600.0 Bytes in 90.0 ms  = 17.36111111111111 MB/Sec 

[Input Filenames]
key, test1

[Output Filenames]
test1.enc, test1.enc.dec



[Test Case 2]

[Command line]
java AES e key2 test2
java AES d key2 test2.enc

[Timing Information]
Encryption Throughput: 1600.0 Bytes in 82.0 ms  = 19.054878048780488 MB/Sec 
Decryption Throughput: 1600.0 Bytes in 79.0 ms  = 19.77848101265823 MB/Sec 

[Input Filenames]
key2, test2

[Output Filenames]
test2.enc, test2.enc.dec



[Test Case 3]

[Command line]
java AES e key3 test3
java AES d key3 test3.enc

[Timing Information]
Encryption Throughput: 1600.0 Bytes in 88.0 ms  = 17.75568181818182 MB/Sec 
Decryption Throughput: 1600.0 Bytes in 99.0 ms  = 15.782828282828282 MB/Sec 

[Input Filenames]
key3, test3

[Output Filenames]
test3.enc, test3.enc.dec


[Test Case 4]

[Command line]
java AES e key4 test4
java AES d key4 test4.enc

[Timing Information]
Encryption Throughput: 1600.0 Bytes in 79.0 ms  = 19.77848101265823 MB/Sec
Decryption Throughput: 1600.0 Bytes in 90.0 ms  = 17.36111111111111 MB/Sec  

[Input Filenames]
key4, test4

[Output Filenames]
test4.enc, test4.enc.dec