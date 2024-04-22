import tensorflow as tf
import numpy as np
import cv2
import ImageStreamer

# camera setup
BASE_IMG_WIDTH = 320
BASE_IMG_HEIGHT = 240
camera = None

# image streaming parameters
stream_frames = False

# model parameters
model = None
path_to_keras_model = r'/home/ubuntu/work/models/self_constructed_w100_h40_no_contrast_train_99_val_97.keras'
input_image_size = (100, 40) # (w, h)
img_height_crop_factor = 1/2

def Initialize(stream_images : bool):
    global stream_frames
    stream_frames = stream_images

    initialize_camera()
    load_model()
    
    if stream_images:
        ImageStreamer.Initialize()
    
def initialize_camera():
    global camera
    camera = cv2.VideoCapture(0)
    camera.set(3, BASE_IMG_WIDTH)
    camera.set(4, BASE_IMG_HEIGHT)

# load the model from the .keras file
def load_model():
    print(f'Loading model from: {path_to_keras_model}')

    global model
    model = tf.keras.models.load_model(path_to_keras_model)
    
# crop the image. This means removing the upper part of the image, width stays the same
def crop_image(image):
    return image[(BASE_IMG_HEIGHT * img_height_crop_factor):BASE_IMG_HEIGHT, 0:BASE_IMG_WIDTH]

def predict():
    _, frame = camera.read()
    
    # preprocess input
    cropped_frame = crop_image(frame)
    
    if stream_frames:
        ImageStreamer.send_single_frame(cropped_frame)
    
    image = cv2.resize(cropped_frame, input_image_size)
    image = np.expand_dims(image, axis=0)

    outcomes = ['forwards', 'right', 'left']
    predictions = model.predict(image)
    prediction = outcomes[np.argmax(predictions)]

    return prediction
