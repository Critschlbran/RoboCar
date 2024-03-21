import tensorflow as tf
import keras
from keras.applications.mobilenet_v3 import preprocess_input, decode_predictions
import numpy as np
from datetime import datetime
import os

#model = keras.applications.MobileNetV3Small(
#    input_shape=None,
#    alpha=1.0,
#    minimalistic=False,
#    include_top=True,
#    weights="imagenet",
#    input_tensor=None,
#    classes=1000,
#    pooling=None,
#    dropout_rate=0.2,
#    classifier_activation="softmax",
#    include_preprocessing=True,
#)
#
#

print('Loading model:')
model = tf.keras.models.load_model('/home/ubuntu/work/models/97_train_90_val.keras')

filenames = os.listdir('./images')
files = []
#
for i in range(0, len(filenames)):
    img_path = './images/' + filenames[i]
    img = keras.utils.load_img(img_path, target_size=(128, 128))
    files.append(keras.utils.img_to_array(img))
    files[i] = np.expand_dims(files[i], axis=0)
    files[i] = preprocess_input(files[i])



preds = []

print('Predicting:')

start = datetime.now()
for file in files:
    preds.append(model.predict(file))
end = datetime.now()

print(filenames)
print(preds)
for pred in preds:
    print(np.argmax(pred))
print('Elapsed time: seconds: ', (end - start).seconds, ' microseconds: ', (end - start).microseconds)
