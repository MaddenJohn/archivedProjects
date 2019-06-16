
# coding: utf-8

# # Homework 5
# In this homework you will improve your convolutional network to overfit less on supertux.
# 
# Development notes: 
# 
# 1) If you are doing your homework in a Jupyter/iPython notebook you may need to 'Restart & Clear Output' after making a change and re-running a cell.  TensorFlow will not allow you to create multiple variables with the same name, which is what you are doing when you run a cell that creates a variable twice.<br/><br/>
# 2) Be careful with your calls to global_variables_initializer(). If you call it after training one network it will re-initialize your variables erasing your training.  In general, double check the outputs of your model after all training and before turning your model in. Ending a session will discard all your variable values.
# 
# ## Part 0: Setup

# In[1]:


import tensorflow as tf
import numpy as np
import util

# Load the data we are giving you
def load(filename, W=64, H=64):
    data = np.fromfile(filename, dtype=np.uint8).reshape((-1, W*H*3+1))
    images, labels = data[:, :-1].reshape((-1,H,W,3)), data[:, -1]
    return images, labels

image_data, label_data = load('tux_train.dat')

print('Input shape: ' + str(image_data.shape))
print('Labels shape: ' + str(label_data.shape))

num_classes = 6


# ## Part 1: Define your convnet
# 
# Make sure the total number of parameters is less than 100,000.

# In[ ]:


# Lets clear the tensorflow graph, so that you don't have to restart the notebook every time you change the network
tf.reset_default_graph()

# Set up your input placeholder
inputs = tf.placeholder(tf.float32, (None,64,64,3))

# Step 1: Augment the training data (try the following, not all might improve the performance)
#  * mirror the image
#  * color augmentations (keep the values to small ranges first then try to expand):
#    - brightness
#    - hue
#    - saturation
#    - contrast

def data_augmentation(I):
    # TODO: Put your data augmentation here
    I = tf.image.random_brightness(I, 10)
    #I = tf.image.random_saturation(I, 0.0, 10.0)
    I = tf.image.random_flip_left_right(I)
    #I = tf.image.random_contrast(I, 0.0, 10.0)
    #I = tf.image.random_hue(I, 0.5)
    return I

# map_fn applies data_augmentation independently for each image in the batch, since we are not croping let's apply the augmentation before whitening, it does make evaluation easier
aug_input = tf.map_fn(data_augmentation, inputs)

# During evaluation we don't want data augmentation
eval_inputs = tf.identity(aug_input, name='inputs')

# Whenever you deal with image data it's important to mean center it first and subtract the standard deviation
white_inputs = (eval_inputs - 100.) / 72.


# Set up your label placeholders
labels = tf.placeholder(tf.int64, (None), name='labels')

outputs = []
losses = []

# Step 4: Define multiple models in your ensemble. You should train an ensemble of 5 models.
# Let's put all variables in a scope, this makes training ensembles easier. Make sure each model in your ensemble has it's own scope and produces an output and loss
with tf.name_scope('model1'), tf.variable_scope('model1'):
    # Step 2: define the compute graph of your CNN here (use your solution to HW4 here)
    #   Add weight regularization (l2-loss)  
    h = tf.contrib.layers.conv2d(white_inputs, 19, (5,5), stride=2, scope="conv1", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.conv2d(h, 30, (5,5), stride=2, scope="conv2", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.conv2d(h, 50, (5,5), stride=2, scope="conv3", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.conv2d(h, 100, (3,3), stride=2, scope="conv4", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.max_pool2d(h, (3,3), stride=2, scope="pool")
    h = tf.contrib.layers.conv2d(h, 6, (1,1), stride=2, activation_fn=None, scope="conv5", weights_regularizer=tf.nn.l2_loss)
    # The input 'h' here should be a   None x 1 x 1 x 6   tensor
    h = tf.contrib.layers.flatten(h)

    loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=h, labels=labels))
    outputs.append(h)
    losses.append(loss)
    
#"""
with tf.name_scope('model2'), tf.variable_scope('model2'):
    # Step 2: define the compute graph of your CNN here (use your solution to HW4 here)
    #   Add weight regularization (l2-loss)  
    h = tf.contrib.layers.conv2d(white_inputs, 19, (5,5), stride=2, scope="conv1", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.conv2d(h, 30, (5,5), stride=2, scope="conv2", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.conv2d(h, 50, (5,5), stride=2, scope="conv3", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.conv2d(h, 100, (3,3), stride=2, scope="conv4", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.max_pool2d(h, (3,3), stride=2, scope="pool")
    h = tf.contrib.layers.conv2d(h, 6, (1,1), stride=2, activation_fn=None, scope="conv5", weights_regularizer=tf.nn.l2_loss)
    # The input 'h' here should be a   None x 1 x 1 x 6   tensor
    h = tf.contrib.layers.flatten(h)

    loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=h, labels=labels))
    outputs.append(h)
    losses.append(loss)
    
with tf.name_scope('model3'), tf.variable_scope('model3'):
    # Step 2: define the compute graph of your CNN here (use your solution to HW4 here)
    #   Add weight regularization (l2-loss)  
    h = tf.contrib.layers.conv2d(white_inputs, 19, (5,5), stride=2, scope="conv1", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.conv2d(h, 30, (5,5), stride=2, scope="conv2", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.conv2d(h, 50, (5,5), stride=2, scope="conv3", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.conv2d(h, 100, (3,3), stride=2, scope="conv4", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.max_pool2d(h, (3,3), stride=2, scope="pool")
    h = tf.contrib.layers.conv2d(h, 6, (1,1), stride=2, activation_fn=None, scope="conv5", weights_regularizer=tf.nn.l2_loss)
    # The input 'h' here should be a   None x 1 x 1 x 6   tensor
    h = tf.contrib.layers.flatten(h)

    loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=h, labels=labels))
    outputs.append(h)
    losses.append(loss)
    
with tf.name_scope('model4'), tf.variable_scope('model4'):
    # Step 2: define the compute graph of your CNN here (use your solution to HW4 here)
    #   Add weight regularization (l2-loss)  
    h = tf.contrib.layers.conv2d(white_inputs, 19, (5,5), stride=2, scope="conv1", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.conv2d(h, 30, (5,5), stride=2, scope="conv2", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.conv2d(h, 50, (5,5), stride=2, scope="conv3", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.conv2d(h, 100, (3,3), stride=2, scope="conv4", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.max_pool2d(h, (3,3), stride=2, scope="pool")
    h = tf.contrib.layers.conv2d(h, 6, (1,1), stride=2, activation_fn=None, scope="conv5", weights_regularizer=tf.nn.l2_loss)
    # The input 'h' here should be a   None x 1 x 1 x 6   tensor
    h = tf.contrib.layers.flatten(h)

    loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=h, labels=labels))
    outputs.append(h)
    losses.append(loss)
    
with tf.name_scope('model5'), tf.variable_scope('model5'):
    # Step 2: define the compute graph of your CNN here (use your solution to HW4 here)
    #   Add weight regularization (l2-loss)  
    h = tf.contrib.layers.conv2d(white_inputs, 19, (5,5), stride=2, scope="conv1", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.conv2d(h, 30, (5,5), stride=2, scope="conv2", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.conv2d(h, 50, (5,5), stride=2, scope="conv3", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.conv2d(h, 100, (3,3), stride=2, scope="conv4", weights_regularizer=tf.nn.l2_loss)
    h = tf.layers.dropout(h)
    h = tf.contrib.layers.max_pool2d(h, (3,3), stride=2, scope="pool")
    h = tf.contrib.layers.conv2d(h, 6, (1,1), stride=2, activation_fn=None, scope="conv5", weights_regularizer=tf.nn.l2_loss)
    # The input 'h' here should be a   None x 1 x 1 x 6   tensor
    h = tf.contrib.layers.flatten(h)

    loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=h, labels=labels))
    outputs.append(h)
    losses.append(loss)
#"""


output = tf.add_n(outputs, name='output')

# Sum up all the losses
loss = tf.add_n(losses)
regularization_loss = tf.losses.get_regularization_loss()
# Let's weight the regularization loss down, otherwise it will hurt the model performance
# You can tune this weight if you wish
total_loss = loss + 1e-6 * regularization_loss

# create an optimizer: Adam might work slightly better (it's a bit faster for Tux)
optimizer = tf.train.AdamOptimizer(0.0005, 0.9, 0.999)

# use that optimizer on your loss function
opt = optimizer.minimize(total_loss)
correct = tf.equal(tf.argmax(output, 1), labels)
accuracy = tf.reduce_mean(tf.cast(correct, tf.float32))

# You're allowed to use 500k variables this time, 100k per model in your ensemble.
print( "Total number of variables used ", np.sum([v.get_shape().num_elements() for v in tf.trainable_variables()]), '/', 500000 )


# ## Part 2: Training
# 
# Training might take up to 20 min depending on your architecture.  This time around you should get close to 100% training accuracy.

# In[ ]:


image_val, label_val = load('tux_val.dat')

# Batch size
BS = 32

# Start a session
sess = tf.Session()

# Set up training
sess.run(tf.global_variables_initializer())

# Train convnet
# Step 3: You should tune the number of epochs to maximize validation accuracy, you can either do this by hand or automate the process.
for epoch in range(50):
    # Let's shuffle the data every epoch
    np.random.seed(epoch)
    np.random.shuffle(image_data)
    np.random.seed(epoch)
    np.random.shuffle(label_data)
    # Go through the entire dataset once
    accuracy_vals, loss_vals = [], []
    for i in range(0, image_data.shape[0]-BS+1, BS):
        # Train a single batch
        batch_images, batch_labels = image_data[i:i+BS], label_data[i:i+BS]
        accuracy_val, loss_val, _ = sess.run([accuracy, total_loss, opt], feed_dict={inputs: batch_images, labels: batch_labels})
        accuracy_vals.append(accuracy_val)
        loss_vals.append(loss_val)

    val_correct = []
    for i in range(0, image_val.shape[0], BS):
        batch_images, batch_labels = image_val[i:i+BS], label_val[i:i+BS]
        val_correct.extend( sess.run(correct, feed_dict={eval_inputs: batch_images, labels: batch_labels}) )
    print('[%3d] Accuracy: %0.3f  \t  Loss: %0.3f  \t  validation accuracy: %0.3f'%(epoch, np.mean(accuracy_vals), np.mean(loss_vals), np.mean(val_correct)))
    if (np.mean(val_correct) > 0.98):
        break


# ## Part 3: Evaluation

# ### Compute the valiation accuracy

# In[ ]:


image_val, label_val = load('tux_val.dat')

print('Input shape: ' + str(image_val.shape))
print('Labels shape: ' + str(label_val.shape))

val_correct = []
for i in range(0, image_val.shape[0], BS):
    batch_images, batch_labels = image_val[i:i+BS], label_val[i:i+BS]
    val_correct.extend( sess.run(correct, feed_dict={eval_inputs: batch_images, labels: batch_labels}) )
print("ConvNet Validation Accuracy: ", np.mean(val_correct))


# ## Part 4: Save Model
# Please note that we also want you to turn in your ipynb for this assignment.  Zip up the ipynb along with the tfg for your submission.

# In[ ]:


util.save('assignment5.tfg', session=sess)


# ### Part 5 (optional): See your model

# In[ ]:


# Show the current graph
util.show_graph(tf.get_default_graph().as_graph_def())

