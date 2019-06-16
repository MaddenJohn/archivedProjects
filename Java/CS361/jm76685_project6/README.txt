UTEID: jm76685;
FIRSTNAME: Jonathan;
LASTNAME: Madden;
CSACCOUNT: jm76685;
EMAIL: jm76685@cs.utexas.edu;

[Program 6]
[Description]
There are 4 java files: In PasswordCrack.java, with the key functions main, getPassword, simpleCheck, complexCheck, and secondSimpleCheck. In 
the main function the basic parsing is done, as well as the creation of threads. In the getPassword function the optimization is done, by 
calling the appropriate functions of simpleCheck, complexCheck, and secondSimpleCheck, for the best performance. In simpleCheck all of the 
possible checks that are one or two encryptions are called, since there are only one combination of each of these. In complexCheck, a check
for all the possible prepends or appends is done, which can be any ascii character and this is why it is done separate. Lastly, in 
secondSimpleCheck, a second mangle is applied to the word, which is done last for the best performance. In Cracker.java, threading is 
the main implementation, which will simply call the getPassword funciton in PasswordCrack.java in the run function for each thread. 
In jcrpt.java all credit does not go to me, since this was taken directly from the assingment page, where it was credited to
Based upon C source code written by Eric Young, eay@psych.uq.oz.au. Lastly, in User.java I outline the user structure to be used to 
hold the data for each user. To compile our program, you need to use "javac *.java". To run our program, you need to use 
java PasswordCrack inputFile1 inputFile2 where inputFile1 is the dictionary and inputFile2 is a list of passwords to crack.

[Finish]
I found 17/20 on passwd1 in time 524.356 seconds. I found 15/20 on passwd2 in time 796.019 seconds.

[Test Case 1]

[Input]
michael:atbWfKL4etk4U:500:500:Michael Ferris:/home/michael:/bin/bash		
abigail:&i4KZ5wmac566:501:501:Abigail Smith:/home/abigail:/bin/tcsh
samantha:(bUx9LiAcW8As:502:502:Samantha Connelly:/home/samantha:/bin/bash
tyler:<qt0.GlIrXuKs:503:503:Tyler Jones:/home/tyler:/bin/tcsh
alexander:feohQuHOnMKGE:504:504:Alexander Brown:/home/alexander:
james:{ztmy9azKzZgU:505:505:James Dover:/home/james:/bin/bash
benjamin:%xPBzF/TclHvg:506:506:Benjamin Ewing:/home/benjamin:/bin/bash
morgan:khnVjlJN3Lyh2:507:507:Morgan Simmons:/home/morgan:/bin/bash
jennifer:e4DBHapAtnjGk:508:508:Jennifer Elmer:/home/jennifer:/bin/bash
nicole:7we09tBSVT76o:509:509:Nicole Rizzo:/home/nicole:/bin/tcsh
evan:3dIJJXzELzcRE:510:510:Evan Whitney:/home/evan:/bin/bash
jack:jsQGVbJ.IiEvE:511:511:Jack Gibson:/home/jack:/bin/bash
victor:w@EbBlXGLTue6:512:512:Victor Esperanza:/home/victor:
caleb:8joIBJaXJvTd2:513:513:Caleb Patterson:/home/caleb:/bin/bash
nathan:nxsr/UAKmKnvo:514:514:Nathan Moore:/home/nathan:/bin/ksh
connor:gwjT8yTnSCVQo:515:515:Connor Larson:/home/connor:/bin/bash
rachel:KelgNcBOZdHmA:516:516:Rachel Saxon:/home/rachel:/bin/bash
dustin:5WW698tSZJE9I:517:517:Dustin Hart:/home/dustin:/bin/csh
maria:!cI6tOT/9D2r6:518:518:Maia Salizar:/home/maria:/bin/zsh
paige:T8jwuve9rQBo.:519:519:Paige Reiser:/home/paige:/bin/bash

[Output]
The password for user Michael Ferris is michael
The password for user Maia Salizar is Salizar
The password for user Abigail Smith is liagiba
The password for user Benjamin Ewing is abort6
The password for user Samantha Connelly is amazing
The password for user Tyler Jones is eeffoc
The password for user Jennifer Elmer is doorrood
The password for user Connor Larson is enoggone
The password for user Evan Whitney is Impact
The password for user Nicole Rizzo is keyskeys
The password for user Jack Gibson is sATCHEL
The password for user Alexander Brown is squadro
The password for user Victor Esperanza is THIRTY
The password for user James Dover is icious
The password for user Morgan Simmons is rdoctor
The password for user Rachel Saxon is obliqu3
The password for user Caleb Patterson is teserP

In total, I can crack 17/20 password in time 524.356 seconds.
I can not crack 3/20 password, the list is
dustin
paige
nathan


[Test Case 2]

[Input]
michael:atQhiiJLsT6cs:500:500:Michael Ferris:/home/michael:/bin/bash		
abigail:&ileDTgJtzCRo:501:501:Abigail Smith:/home/abigail:/bin/tcsh
samantha:(bt0xiAwCf7nA:502:502:Samantha Connelly:/home/samantha:/bin/bash
tyler:<qf.L9z1/tZkA:503:503:Tyler Jones:/home/tyler:/bin/tcsh
alexander:fe8PnYhq6WoOQ:504:504:Alexander Brown:/home/alexander:
james:{zQOjvJcHMs7w:505:505:James Dover:/home/james:/bin/bash
benjamin:%xqFrM5RVA6t6:506:506:Benjamin Ewing:/home/benjamin:/bin/bash
morgan:kh/1uC5W6nDKc:507:507:Morgan Simmons:/home/morgan:/bin/bash
jennifer:e4EyEMhNzYLJU:508:508:Jennifer Elmer:/home/jennifer:/bin/bash
nicole:7wKTWsgNJj6ac:509:509:Nicole Rizzo:/home/nicole:/bin/tcsh
evan:3d1OgBYfvEtfg:510:510:Evan Whitney:/home/evan:/bin/bash
jack:js5ctN1leUABo:511:511:Jack Gibson:/home/jack:/bin/bash
victor:w@FxBZv.d0y/U:512:512:Victor Esperanza:/home/victor:
caleb:8jGWbU0xbKz06:513:513:Caleb Patterson:/home/caleb:/bin/bash
nathan:nxr9OOqvZjbGs:514:514:Nathan Moore:/home/nathan:/bin/ksh
connor:gw9oXmw1L08RM:515:515:Connor Larson:/home/connor:/bin/bash
rachel:KenK1CTDGr/7k:516:516:Rachel Saxon:/home/rachel:/bin/bash
dustin:5Wb2Uqxhoyqfg:517:517:Dustin Hart:/home/dustin:/bin/csh
maria:!cSaQELm/EBV.:518:518:Maia Salizar:/home/maria:/bin/zsh
paige:T8U5jQaDVv/o2:519:519:Paige Reiser:/home/paige:/bin/bash

[Output]
The password for user Samantha Connelly is cOnNeLlY
The password for user Jennifer Elmer is ElmerJ
The password for user Abigail Smith is Saxon
The password for user Connor Larson is nosral
The password for user Jack Gibson is ellows
The password for user Morgan Simmons is dIAMETER
The password for user Tyler Jones is eltneg
The password for user Nicole Rizzo is INDIGNITIES
The password for user Michael Ferris is tremors
The password for user Caleb Patterson is zoossooz
The password for user Benjamin Ewing is soozzoos
The password for user Evan Whitney is ^bribed
The password for user James Dover is enchant$
The password for user Alexander Brown is Lacque
The password for user Dustin Hart is Swine3


In total, I can crack 15/20 password in time 796.019 seconds.
I can not crack 5/20 password, the list is
maria
paige
nathan
victor
rachel
