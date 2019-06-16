Name: Jonathan Madden
UTEID: jm76685

For question 1 I based by evaluation function on the position of the ghosts,
the position of the nearest food, the current score and the position of
the nearest capsule. I used the reciprocals of the nearest food and
the nearest capsule and added all four of these aspects to calculate
the evaluation function. In cases where the ghost was within 3 spaces, then
I would force the pacman to go in the direction farthest from the ghost. If
a capsule was eaten, then the ghosts were ignored, and would be eaten if they
happened to be in the line of the path of pacman.  

For questions 2-4 I used the pseudocode in the book and in the slides to
formulate the algorithms. These were very similar, with the only major 
difference being to take into consideration the depth and multiple ghosts. 
To handle multiple ghosts I kept track of the ghost index and would call
the minimum function multiple times to go through each of the ghosts.

For the last question, q5, I used four variables in determining the 
new evaluation function. These four were the two furthests food dots and 
pacmans distance to the closest of these two, the distance to the nearest
ghost, the distance to the nearest capsule, and the score. I combined these
for a linear sum, taking an appropriate percentage of each to maximize the
score of pacman. 