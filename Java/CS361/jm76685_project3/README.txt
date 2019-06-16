UTEID: jm76685;
FIRSTNAME: Jonathan;
LASTNAME: Madden;
CSACCOUNT: jm76685;
EMAIL: jm76685@cs.utexas.edu;

[Program 3]
[Description]
There is 1 java file: I implemented everything myself. First, the main function handles the parsing of the command line arguments, calling
the appropriate function based on this and printing error for invalid arguments. If the readPicture function is called, then the main decoding
algorithm will be run. This algorithm reads each of the three rgb values for a pixel and adds these two an array of bits. This array is 
interpreted as 3 bytes and when filled, will write the appropriate data to be stored later for the final write to the message-out. This
method also checks for a zero byte and if found then the message has ended and the function will end. If the writeToPicture function is called
then a similar process will happen, reading the rgb values, and reading the value of the message, but this time the rgb values will be 
modified for a new image to be stored. This image will have updated rgb values storing the message as odd or even numbers. If the message
is too long, then it will be truncated and a message will be printed to console. This
Program is tested and works perfectly on bmp files, such as the one given for example.

[Finish]
I finished all of the project.

[Questions&Answers]

[Question 1]
Comparing your original and modified images carefully, can you detect *any* difference visually (that is, in the appearance of the image)?

[Answer 1]
No, the image looks exactly the same.

   
[Question 2]
Can you think of other ways you might hide the message in image files (or in other types of files)?

[Answer 2]
One way to hide a message might be to use a particular section of the picture, such as a black section and modify these values to a new
rgb value that is specific to your desired encoding. Then whenever this value is seen, then you can encode a particular size block of this
section looking only for this specific rgb value and representing each one with this value as a 1 and black ones as a 0. This way would
be uniform, in comparison to encoding the entire image, which might make it harder to detect. 


[Question 3]
Can you invent ways to increase the bandwidth of the channel?

[Answer 3]
Essentially, right now we only check the last bit of the 8 bit rgb value, it being even or odd is based on this bit. However, we
could use 2 of these bits instead of 1, effectively increasing our bandwidth by 4 times, and allowing 12 bits per pixel instead of 3.
This would just have to be interpreted later through bit shifting to get these last 2 bits and using them correctly. 



[Question 4]
Suppose you were tasked to build an "image firewall" that would block images containing hidden messages. Could you do it? 
How might you approach this problem?

[Answer 4]
I could not build a perfect image firewall, but some methods such as the one in this project could be prevented. This could be done easily by
checking various possibly known methods of concealment, such as through even and odd bits on the image or even %7 or some other possible schema
and if the image is verified to have a certain amount of readability then mark it as containing a hidden message. 


[Question 5]
Does this fit our definition of a covert channel? Explain your answer.

[Answer 5]
No, a covert channel is a path for the flow of information between subjects within a system, 
utilizing system resources that were not designed to be used for inter-subject communication. 
While this is a method of communication, if a subject can send a picture to another subject in a system, 
then this means that they are already allowed to send them information, since the picture itself is a form
of communication, regardless if it has a hidden message or not. Even without the hidden message, a message could
easily be sent in a picture of words because this would be allowed in this system, meaning this is not a covert channel
but just a means of hiding the message content of the message, but not a restriction of the flow of information.

