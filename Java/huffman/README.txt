README.txt
HuffMark Test Results & Analysis
_______________________________________________________________________________

Name: Jonathan Madden 
UTEID: JM76685
Email: johnmadden4477@yahoo.com

Name: Khiem Tang 
UTEID: KLT2399
Email: tang.khiem@yahoo.com

Section Number: 51740

Estimated Work Time: 17 hours
_______________________________________________________________________________

HuffMark tests for the Calgary directory:

compressing to: C:\Users\klt\workspace\HuffmanCoding\calgary\bib.hf
bib from	 111261 to	 73795 in	 0.134
compressing to: C:\Users\klt\workspace\HuffmanCoding\calgary\book1.hf
book1 from	 768771 to	 439409 in	 0.630
compressing to: C:\Users\klt\workspace\HuffmanCoding\calgary\book2.hf
book2 from	 610856 to	 369335 in	 0.522
compressing to: C:\Users\klt\workspace\HuffmanCoding\calgary\geo.hf
geo from	 102400 to	 73592 in	 0.107
compressing to: C:\Users\klt\workspace\HuffmanCoding\calgary\news.hf
news from	 377109 to	 247428 in	 0.351
compressing to: C:\Users\klt\workspace\HuffmanCoding\calgary\obj1.hf
obj1 from	 21504 to	 17085 in	 0.028
compressing to: C:\Users\klt\workspace\HuffmanCoding\calgary\obj2.hf
obj2 from	 246814 to	 195131 in	 0.274
compressing to: C:\Users\klt\workspace\HuffmanCoding\calgary\paper1.hf
paper1 from	 53161 to	 34371 in	 0.053
compressing to: C:\Users\klt\workspace\HuffmanCoding\calgary\paper2.hf
paper2 from	 82199 to	 48649 in	 0.072
compressing to: C:\Users\klt\workspace\HuffmanCoding\calgary\paper3.hf
paper3 from	 46526 to	 28309 in	 0.042
compressing to: C:\Users\klt\workspace\HuffmanCoding\calgary\paper4.hf
paper4 from	 13286 to	 8894 in	 0.014
compressing to: C:\Users\klt\workspace\HuffmanCoding\calgary\paper5.hf
paper5 from	 11954 to	 8465 in	 0.015
compressing to: C:\Users\klt\workspace\HuffmanCoding\calgary\paper6.hf
paper6 from	 38105 to	 25057 in	 0.038
compressing to: C:\Users\klt\workspace\HuffmanCoding\calgary\pic.hf
pic from	 513216 to	 107586 in	 0.167
compressing to: C:\Users\klt\workspace\HuffmanCoding\calgary\progc.hf
progc from	 39611 to	 26948 in	 0.041
compressing to: C:\Users\klt\workspace\HuffmanCoding\calgary\progl.hf
progl from	 71646 to	 44017 in	 0.075
compressing to: C:\Users\klt\workspace\HuffmanCoding\calgary\progp.hf
progp from	 49379 to	 31248 in	 0.050
compressing to: C:\Users\klt\workspace\HuffmanCoding\calgary\trans.hf
trans from	 93695 to	 66252 in	 0.096
--------
total bytes read: 3251493
total compressed bytes 1845571
total percent compression 43.239
compression time: 2.709

Analysis: This directory featured a variety of generic file types that contained different texts of different
sizes. Compared to the other directories, this one featured the highest compression percentage at 43.239%, which
is most likely evident because the files all consisted of all generic file formats that could be accessed and seen
as characters. Due to the redundancy of the text files in terms of the characters, and the fact that the Huffman
encoding method processes data in a way that removes redundancy, the results showed that compressing
was a fairly quick process. 

What was most noticeable about these results was the output of the pic.hf file.  As shown, the compression percentage
for this file was 79.03%, much higher than the rest. A possible conclusion for this massive change in size would be that
the file is a picture which contains a variety of characters, with types that extend beyond regular legible characters
written in text files (alphabet). With these characters being converted to 1s and 0s through the program, the size is 
significantly decreased as it takes less space to store the numbers versus the characters.

It was also interesting to note that the pic file seemed to compress faster than the news file (0.167 versus 0.351),
despite the pic being larger than the news file by nearly 200,000 bytes.  This might be because the pic file contained 
a high amount of redundant white space, which made compressing these characters easier since they were more quickly sorted
into the frequency array.  The news file contained more diverse and condensed character data and text.
_______________________________________________________________________________

HuffMark tests for the BooksAndHTML directory:

compressing to: C:\Users\klt\workspace\HuffmanCoding\booksandhtml\A7_Recursion.html.hf
A7_Recursion.html from	 41163 to	 26189 in	 0.057
compressing to: C:\Users\klt\workspace\HuffmanCoding\booksandhtml\CiaFactBook2000.txt.hf
CiaFactBook2000.txt from	 3497369 to	 2260664 in	 3.292
compressing to: C:\Users\klt\workspace\HuffmanCoding\booksandhtml\jnglb10.txt.hf
jnglb10.txt from	 292059 to	 168618 in	 0.241
compressing to: C:\Users\klt\workspace\HuffmanCoding\booksandhtml\kjv10.txt.hf
kjv10.txt from	 4345020 to	 2489768 in	 3.566
compressing to: C:\Users\klt\workspace\HuffmanCoding\booksandhtml\melville.txt.hf
melville.txt from	 82140 to	 47364 in	 0.066
compressing to: C:\Users\klt\workspace\HuffmanCoding\booksandhtml\quotes.htm.hf
quotes.htm from	 61563 to	 38423 in	 0.056
compressing to: C:\Users\klt\workspace\HuffmanCoding\booksandhtml\rawMovieGross.txt.hf
rawMovieGross.txt from	 117272 to	 53833 in	 0.076
compressing to: C:\Users\klt\workspace\HuffmanCoding\booksandhtml\revDictionary.txt.hf
revDictionary.txt from	 1130523 to	 611618 in	 0.867
compressing to: C:\Users\klt\workspace\HuffmanCoding\booksandhtml\syllabus.htm.hf
syllabus.htm from	 33273 to	 21342 in	 0.032
compressing to: C:\Users\klt\workspace\HuffmanCoding\booksandhtml\ThroughTheLookingGlass.txt.hf
ThroughTheLookingGlass.txt from	 188199 to	 110293 in	 0.156
--------
total bytes read: 9788581
total compressed bytes 5828112
total percent compression 40.460
compression time: 8.409

Analysis: This directory featured text and html files.  This directory had the second fastest compression
rate with 40.460%, and once again, it is mostly attributed to the fact that there were basic text files
that were compressed rather than more complex files.  Looking at the results, the txt and html files seemed
to not present any noticeable differences when compressing, in time or percentage compressed. However, the text files
seemed to have a higher frequency of characters in common compared to the html files. Since the html files were primarily
text though, it did not contribute much to the compression.
_______________________________________________________________________________

HuffMark tests for the Waterloo directory:

compressing to: C:\Users\klt\workspace\HuffmanCoding\waterloo\clegg.tif.hf
clegg.tif from	 2149096 to	 2034595 in	 2.924
compressing to: C:\Users\klt\workspace\HuffmanCoding\waterloo\frymire.tif.hf
frymire.tif from	 3706306 to	 2188593 in	 3.098
compressing to: C:\Users\klt\workspace\HuffmanCoding\waterloo\lena.tif.hf
lena.tif from	 786568 to	 766146 in	 1.067
compressing to: C:\Users\klt\workspace\HuffmanCoding\waterloo\monarch.tif.hf
monarch.tif from	 1179784 to	 1109973 in	 1.547
compressing to: C:\Users\klt\workspace\HuffmanCoding\waterloo\peppers.tif.hf
peppers.tif from	 786568 to	 756968 in	 1.045
compressing to: C:\Users\klt\workspace\HuffmanCoding\waterloo\sail.tif.hf
sail.tif from	 1179784 to	 1085501 in	 1.516
compressing to: C:\Users\klt\workspace\HuffmanCoding\waterloo\serrano.tif.hf
serrano.tif from	 1498414 to	 1127645 in	 1.561
compressing to: C:\Users\klt\workspace\HuffmanCoding\waterloo\tulips.tif.hf
tulips.tif from	 1179784 to	 1135861 in	 1.568
--------
total bytes read: 12466304
total compressed bytes 10205282
total percent compression 18.137
compression time: 14.326

Analysis: This directory contained all tif files, or picture files.  This directory took the longest to compress,
and also had the lowest compression rate with 18.137%. A possible conclusion for the slow compression rate is most
likely the file size. When opening these files in a text editor, it was evident that a wide range of characters was
present with a low redundancy rate. In addition, to explain the low compression percentage, tif files are high quality
graphics files, so it's possible that each individual pixel has more details than the usual 256 for characters
in containing the color.  Thus, pixels that look the same are different in terms of binary data, making it difficult 
to compress.  

Looking at the individual comparisons of the pictures when compressed, the frymire.tif picture seemed to have the highest
compression rate with 40.9%. It was noticed that this tif file was the only one in the directory that featured a high amount
of white and black pixels (can be seen on the bottom left of the picture). Pictures that are white most likely yield
redundant character combinations, leading to higher compression rates, compared to pictures with a wide spectrum of color.
_______________________________________________________________________________

What happens what you try to comprses a huffman code file?

Once redundancy is removed from a file through compressing it the first time, it cannot be compressed much further. As a 
result the amount of compression the second time is much less.

Summary of Analysis: The calgary directory displayed the highest compression rate, and the Waterloo directory displayed
the lowest rate. This can be concluded to the fact that the generic files were less in size, as well as higher in redundant
characters than the tif files, making them more susceptible to high compression rates when placed through the program. The Huffman
program, based on its method of compression by taking redundant data and reducing it to smaller, more manageable binary bits,
it seems to run most efficiently on files with more relative / similar character types.  