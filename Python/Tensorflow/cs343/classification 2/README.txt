Name: Jonathan Madden
UTEID: jm76685

For question one I went through and classified all of the training data and used this as the yprime data to be compared to.
The y, which was the other compariosn data was found from the training label, and each of the yPrimes were used in comparison.
If different values were found, then the weight values were updated. 

For question 2, I simply appended the first 100 elements of a sorted list of the weights by the specific label and returned this
list. Then I answered the question by looking at the output.

For question 3, I followed the same actions as in question 1, but added in the utility of multiplying by the specific formula
found on the assignment page. 

For question 4, I added one one feature which was whether or not a specific number had one or more white regions. To do this, 
I implemented a recursive algorithm to check for the number of white regions, setting the end feature to 0 or 1 based on this number.

For question 5, I used the same code as in question 1 except i modified where I updated the weights so that the updates would not 
be using vectors in the same way. 

For question 6, I added two features, closest food and closest ghost, which simply added their distances to the features list. Both
of these values were inverted for them to improve the performance.