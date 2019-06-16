
# coding: utf-8

# In[1]:


#get_ipython().magic('pylab inline')


# # Homework 8
# Let's draw some pictures today.
# 
# ## Part 0: Setup

# In[2]:


import tensorflow as tf
import numpy as np
import util

# Colors to visualize the labeling
COLORS = np.array([(0,0,0), (255,0,0), (0,255,0), (255,255,0), (0,0,255), (255,255,255)], dtype=np.uint8)
CROP_SIZE = 64

def parser(record):
    # Parse the TF record
    parsed = tf.parse_single_example(record, features={
        'height': tf.FixedLenFeature([], tf.int64),
        'width': tf.FixedLenFeature([], tf.int64),
        'image_raw': tf.FixedLenFeature([], tf.string),
        'label_raw': tf.FixedLenFeature([], tf.string)
    })
    # Load the data and format it
    H = tf.cast(parsed['height'], tf.int32)
    W = tf.cast(parsed['width'], tf.int32)
    image = tf.reshape(tf.decode_raw(parsed["image_raw"], tf.uint8), [H,W,3])
    label = tf.reshape(tf.decode_raw(parsed["label_raw"], tf.uint8), [H,W])
    
    ## Data augmentation
    # Stack the image and labels to make sure the same operations are applied
    data = tf.concat([image, label[:,:,None]], axis=-1)
    
    # TODO: Apply the data augmentation (copy from HW7)
    data = tf.image.random_flip_left_right(data)
    tf.random_crop(data, [H,W,4])
    
    return data[:,:,:-1], data[:,:,-1]

def load_dataset(tfrecord):
    # Load the dataset
    dataset = tf.contrib.data.TFRecordDataset(tfrecord)

    # Parse the tf record entries
    dataset = dataset.map(parser, num_threads=8, output_buffer_size=1024)

    # Shuffle the data, batch it and run this for multiple epochs
    dataset = dataset.shuffle(buffer_size=10000)
    dataset = dataset.batch(32)
    dataset = dataset.repeat()
    return dataset

# We still have 6 classes
num_classes = 6


# ## Part 1: Define your convnet

# In[3]:


# Create a new log directory (if you run low on disk space you can either disable this or delete old logs)
# run: `tensorboard --logdir log` to see all the nice summaries
for n_model in range(1000):
    LOG_DIR = 'log/model_%d'%n_model
    from os import path
    if not path.exists(LOG_DIR):
        break

# Lets clear the tensorflow graph, so that you don't have to restart the notebook every time you change the network
tf.reset_default_graph()

TF_COLORS = tf.constant(COLORS)

train_data = load_dataset('train.tfrecord')
valid_data = load_dataset('valid.tfrecord')

# Create an iterator for the datasets
# The iterator allows us to quickly switch between training and validataion
iterator = tf.contrib.data.Iterator.from_structure(train_data.output_types, ((None,None,None,3), (None,None,None)))

# and fetch the next images from the dataset (every time next_image is evaluated a new image set of 32 images is returned)
next_image, next_label = iterator.get_next()

# Define operations that switch between train and valid
switch_train_op = iterator.make_initializer(train_data)
switch_valid_op = iterator.make_initializer(valid_data)

# Convert the input
image = tf.cast(next_image, tf.float32)
label = tf.cast(next_label, tf.int32)

# Define the labels and whiten them in 1-hot
label = tf.identity(label, name='label')
one_hot_label = tf.one_hot(label, num_classes) - np.array([ 0.66839117, 0.00382957, 0.00092516, 0.00345217, 0.00339063, 0.3200113 ])[None,None,None,:]

# Whiten the image
white_image = (image - 100.) / 72.

# Let's produce the low resolution image and whiten it
image_lr = tf.layers.average_pooling2d(image, 5, 4, padding='SAME')
image_lr = tf.identity(image_lr, name='image_lr')
white_lr = (image_lr - 100.) / 72.

# TODO: Define your convnet here (You can model this similar to HW7)

newImage = tf.image.resize_images(
    white_lr,
    [256,256],
    align_corners=False
)

h = newImage 
training = tf.placeholder_with_default(False, (), name='training')
count = 23
iterations = 4
hs = []
for i in range(iterations):
   h = tf.contrib.layers.conv2d(h, count, (5, 5), weights_regularizer=tf.nn.l2_loss)
   h = tf.layers.batch_normalization(h, center=False, scale=False, training=training)
for i in range(iterations):
    hs.append(h)
    h = tf.contrib.layers.conv2d(h, count*int(1.5**i), (5,5), stride=(2,2), weights_regularizer=tf.nn.l2_loss, scope='conv%d'%(i+1))
    h = tf.layers.batch_normalization(h, center=False, scale=False, training=training)

for i in range(iterations)[::-1]:
    h = tf.contrib.layers.conv2d_transpose(h, count*int(1.5**i), (5,5), stride=(2,2), weights_regularizer=tf.nn.l2_loss, scope='upconv%d'%(i+1))
    h = tf.layers.batch_normalization(h, center=False, scale=False, training=training)
    h = tf.concat([h, hs[i]], axis=-1)

h = tf.contrib.layers.conv2d(h, 3, (1,1), scope='cls', activation_fn=None)

"""
# 4 conv layers
for i in range(iterations):
   h = tf.contrib.layers.conv2d(h, count, (5, 5), weights_regularizer=tf.nn.l2_loss)
   h = tf.layers.batch_normalization(h, center=False, scale=False, training=training)

# 4 up conv layers
for i in range(iterations):
    h = tf.contrib.layers.conv2d(h, count, (5, 5), stride=(2, 2))
    h = tf.layers.batch_normalization(h, center=False, scale=False, training=training)
    h = tf.contrib.layers.conv2d_transpose(h, count, (5, 5), stride=(2, 2))

h = tf.contrib.layers.conv2d(h, 3, (5, 5))
"""
# Let's compute the output labeling
output = tf.cast(tf.clip_by_value(72.*h + 100., 0, 255), tf.uint8, name='output')

# Define the loss function
loss = tf.reduce_mean(tf.abs(white_image - h))

# Let's weight the regularization loss down, otherwise it will hurt the model performance
# You can tune this weight if you wish
regularization_loss = tf.losses.get_regularization_loss()
total_loss = loss + 1e-6 * regularization_loss

# Adam will likely converge much faster than SGD for this assignment.
optimizer = tf.train.AdamOptimizer(0.001, 0.9, 0.999)

# use that optimizer on your loss function (control_dependencies makes sure any 
# batch_norm parameters are properly updated)
with tf.control_dependencies(tf.get_collection(tf.GraphKeys.UPDATE_OPS)):
    opt = optimizer.minimize(total_loss)

# Let's define some summaries for tensorboard
colored_label = tf.gather_nd(TF_COLORS, label[:,:,:,None])
tf.summary.image('image', next_image, max_outputs=3)
tf.summary.image('label', colored_label, max_outputs=3)
tf.summary.image('output', output, max_outputs=3)
tf.summary.image('image_lr', image_lr, max_outputs=3)
tf.summary.scalar('loss', tf.placeholder(tf.float32, name='loss'))
tf.summary.scalar('val_loss', tf.placeholder(tf.float32, name='val_loss'))

merged_summary = tf.summary.merge_all()
summary_writer = tf.summary.FileWriter(LOG_DIR, tf.get_default_graph())

# Let's compute the model size
print( "Total number of variables used ", np.sum([v.get_shape().num_elements() for v in tf.trainable_variables()]) )


# ## Part 2: Training
# 
# Training might take up to 20 min depending on your architecture (and if you have a GPU or not).

# In[4]:


# Start a session
sess = tf.Session()

# Set up training
sess.run(tf.global_variables_initializer())

# Run the training for some iterations (play with this , you might want to lower the number of iterations for prototyping)
for it in range(300):
    sess.run(switch_train_op)

    loss_vals = []
    # Run 10 training iterations and 1 validation iteration
    for i in range(10):
        loss_val, _ = sess.run([loss, opt])
        loss_vals.append(loss_val)
    
    sess.run(switch_valid_op)
    loss_val = sess.run(loss)

    # Let's update tensorboard
    summary_writer.add_summary( sess.run(merged_summary, {'loss:0': np.mean(loss_vals), 'val_loss:0': loss_val}), it )
    print('[%3d] Loss: %0.3f  \t  val loss A.: %0.3f'%(it, np.mean(loss_vals), loss_val))    
    if (loss_val < 0.12):
        name = 'assignment8_' + str(int(1000 * loss_val)) + '.tfg'
        util.save(name, session=sess)


# ## Part 3: Evaluation
# ### Compute the validation accuracy

# In[ ]:


total_lbl, total_cor = np.zeros(6)+1e-10, np.zeros(6)
I0 = tf.placeholder(tf.float32, shape=(1, None, None, 3))
LR = tf.layers.average_pooling2d(I0, 5, 4, padding='SAME', name='image_lr')

losses = []
for it in tf.python_io.tf_record_iterator('valid.tfrecord'):
    example = tf.train.Example()
    example.ParseFromString(it)
    I = np.frombuffer(example.features.feature['image_raw'].bytes_list.value[0], dtype=np.uint8).reshape(256, 256, 3)
    L = np.frombuffer(example.features.feature['label_raw'].bytes_list.value[0], dtype=np.uint8).reshape(256, 256)
    
    lr_val = sess.run(LR, {I0: I[None]})
    r = sess.run('output:0', {'image_lr:0':lr_val, 'label:0': L[None]})[0]
    losses.append(np.mean(np.abs(r.astype(np.float32)-I)))
print( 'Mean absolute difference', np.mean(losses) )


# ## Part 4: Save Model
# Please note that we also want you to turn in your ipynb for this assignment.  Zip up the ipynb along with the tfg for your submission.

# In[ ]:


util.save('assignment8.tfg', session=sess)

