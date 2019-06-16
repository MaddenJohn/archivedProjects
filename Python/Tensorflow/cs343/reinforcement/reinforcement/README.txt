Name: Jonathan Madden
UTEID: jm76685

For Question 1, I relied on the formulas in the slides to code this algorithm. This helped in writing
the methods computeQValueFromValues, computeActionFromValues, and the initializing. There was also the
resource from sutton that helped in specifically coding the initializing. The key with the initializing
was to remember to create a copy with the new values and after completing an iteration actually modify 
self.values. This changed the values all at once so they would not effect each other in the iteration. 

For question 2 I realized that if there is no noise then pacman would go for the larger reward. 

For question 3, these were all simly questions that involved critical thinking of what the discount or 
noise variable would be. I simply thought these through and filled them in appropriately.

For question 4, again I relied on the slides and also the formulas listed in learningAgent to solve these
functions. First I had to set the weights as a counter, but used the state and the action for the key. Then
I could base the other functions on this, translating the formulas from the slides into useable code for pacman.

For question 5, I followed along the description using the functions to generate a random chance, with random
action, otherwise picking the best function using computeActionFromQValues

On question 6, I realized that there was no solution, so this was a simple problem.

On question 7, The algorithms that I had already used worked perfectly, with 100% of the time winning so I actually
did not have to modify anything

For question 8, I followed the formula given in the instrucitons, which involved using a mapping of the each of the
features as key on the weights, but worked after implementaion. 