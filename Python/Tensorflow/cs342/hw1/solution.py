import tensorflow as tf
import util

# Create the input placeholder and name it 'input'
I = tf.placeholder(tf.float32, (None,2), name='input')

# Compute PI
pi = tf.reduce_mean(tf.cast(I[:,0]*I[:,0]+I[:,1]*I[:,1] < 1, tf.float32))

# Extra credit, you can integrate out the x or y axis to get a more accurate estimate of pi
pi = tf.reduce_mean(tf.cast(tf.sqrt(1-I*I), tf.float32))

# More extra credit, you can reuse the random variables to a certain degree, by using both x and 1-x and by shifting them and removing the most significant bit, if not for numerical issues, this approach would work with just a single random variable (in fact it does roughtly 90% of the time)
# Your classmate Joe came up with the original idea for this.

x = I
list_pi = []
for i in range(20):
  # Estimate pi using both x and 1-x
  pi = (tf.reduce_mean(tf.cast(tf.sqrt(1-x*x), tf.float32)) + tf.reduce_mean(tf.cast(tf.sqrt((2-x)*x), tf.float32)))/2
  list_pi.append(pi)
  # Remove the most significant bit (and use the lower bits)
  x = x * 2
  x -= tf.floor(x)
# Pi the the average of all bit-shifted versions in list_pi
pi = tf.reduce_mean(list_pi)

# Let's make sure the output is named
output = tf.identity(pi, name='output')

# Save the TF graph
util.save('assignment1.tfg')
