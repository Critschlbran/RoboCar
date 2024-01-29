import tensorflow as tf
import keras
import matplotlib.pyplot as plt
from keras.applications.mobilenet_v3 import preprocess_input

# force tf to use the cpu. Mainly done for performance comparison
#tf.config.set_visible_devices([], 'GPU')

batch_size = 32
img_width = 80
img_height = 80

data_dir = '/mnt/d/Dev/DHBW/DHBW_Studienarbeit_NN_Development/images/per_label'

train_ds = keras.utils.image_dataset_from_directory(
    data_dir,
    label_mode = 'categorical',
    validation_split = 0.1,
    subset = 'training',
    seed = 123,
    image_size = (img_height, img_width),
    batch_size = batch_size
)

#train_ds = keras.utils.to_categorical(train_ds, 3)

val_ds = keras.utils.image_dataset_from_directory(
    data_dir,
    label_mode = 'categorical',
    validation_split = 0.1,
    subset = 'validation',
    seed = 123,
    image_size = (img_height, img_width),
    batch_size = batch_size
)

#val_ds = keras.utils.to_categorical(val_ds, 3)

print(train_ds.class_names)

IMG_SIZE = (img_height, img_width)
IMG_SHAPE = IMG_SIZE + (3,)

base_model = tf.keras.applications.MobileNetV3Small(input_shape=IMG_SHAPE,
                                               include_top=False,
                                               weights='imagenet')

base_model.trainable = False

global_average_layer = tf.keras.layers.GlobalAveragePooling2D()
prediction_layer = tf.keras.layers.Dense(3, activation = 'softmax')

inputs = keras.Input(shape = (img_height, img_width, 3))
x = preprocess_input(inputs)
x = base_model(x, training = False)
x = global_average_layer(x)
outputs = prediction_layer(x)
x = tf.keras.layers.Dropout(0.05)(x)
model = keras.Model(inputs, outputs)

print('Base model layers {}'.format(len(base_model.layers)))

model.summary()

base_learning_rate = 0.02

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

initial_epochs = 25

history = model.fit(train_ds, epochs=initial_epochs, validation_data=val_ds)


base_model.trainable = True
fine_tune_from = len(base_model.layers) - 20

for layer in base_model.layers[:fine_tune_from]:
    layer.trainable = False

# don't train the dense layer
model.layers[len(model.layers) - 1].trainable = False

model.summary()

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate/1000),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(train_ds,
                    epochs=initial_epochs + 10, 
                    initial_epoch=history.epoch[-1], 
                    validation_data=val_ds)