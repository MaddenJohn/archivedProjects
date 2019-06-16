Name: Jonathan Madden
UTEID: jm76685

For Question 1 there were two main problems that I solved, first being the updating of the beliefs based
on the observation and the second was in the case that a noise was None. These were simple fixes, since there
was no resampling required.

For Question 2, I implemented the time elsapse for exact inference. I do this by looping through legalPositions
and updating them based on a possible new position. I also multiply beliefs by probability and normalize this to get 
new beliefs.

Question 3 worked in the busters Agents file. To solve this I got the most likely position for this set of beliefs 
of this ghost, and then found the closest ghost. I then use this to find the best action based on closest Ghost.

Question 4 begins the particle filtering parts of this homework. To start I implemented the initializeUniformly, 
getBeliefDistribution, and observe functions to do their respective goals. In initializeUniformly I Initialize based 
on legal positions the number of Particles required. In observe I loop through and update a new counter for the beliefs
and then use these beliefs to resample. In getdistribution I use the count of the particles to return a distribution, or
returning the position of the jail in case of eating a ghost. 

Question 5 was the time elapse for particle filtering. This was done by looping through all the different combinations,
taking into consideration their probabilities and ultimitaley using these results to resample the particles. 

Question 6 begins the joint particle filter observations, involving the methods initializeParticles, getBeliefDistribution,
 and observeState. In intitializeParticles I first calculate all the possible particles using itertools functions and then
 create particles based on this. In getBeliefDistribution I simply normalize the count of all these different particles. In 
 observe, I loop through each particle in beliefs, and each ghost for the particle, updating the belief of this. If a ghost 
 is eaten, I modify all particles to have the approprate representation of being in jail. Lastly, reinitialize if all particles 
 recieve zero weight or resample if needed
 
 Lastly for Qeustion 7, I update each of the entries in newParticle, using util.sample based on the probability 
 of that position.