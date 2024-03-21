import tensorflow as tf
import keras
import numpy as np
from datetime import datetime
import os
import cv2
from PIL import Image
import ImageStreamer

STREAMING_IMAGE_WIDTH = 320
STREAMING_IMAGE_HEIGHT = 240
camera = cv2.VideoCapture(0)
camera.set(3, STREAMING_IMAGE_WIDTH)
camera.set(4, STREAMING_IMAGE_HEIGHT)

ImageStreamer.initialize()

def load_model():
    print('Loading model:')
    model = tf.keras.models.load_model('/home/ubuntu/work/models/w100_h40_crop_no_contrast_97_val_99_train.keras')
    return model

def crop_image(image):
    return image[120:240, 0:320]

def increase_contrast(image):
    return np.clip(1.4 * image, 0, 255).astype(np.uint8)

def predict(model):
    _, frame = camera.read()
    
    #process input
    cropped_frame = crop_image(frame)
    print(cropped_frame.shape)
    ImageStreamer.send_single_frame(cropped_frame)
    image = cv2.resize(cropped_frame, (100, 40))
    #image = increase_contrast(image)

    image = np.expand_dims(image, axis=0)
    #frame = preprocess_input(frame)

    outcomes = ['forwards', 'right', 'left']
    preds = model.predict(image)
    pred = outcomes[np.argmax(preds)]

    return pred
