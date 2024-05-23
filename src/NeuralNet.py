import tensorflow as tf
import numpy as np
import cv2
import ImageStreamer
import getpass

# camera setup
BASE_IMG_WIDTH = 320
BASE_IMG_HEIGHT = 240
camera = None

# image streaming parameters
stream_frames = False

# model parameters
model = None
# important: adjust the image preprocessing according to the model you are using. The self constructed models need the gray scale image to have only one channel
# whereas the mobilenet needs the images to have three channels. There are functions for both options. Make sure you use the right one.
path_to_keras_model = r'/home/admin/work/models/model.keras'
input_image_size = (100, 40) # (w, h)
img_height_crop_factor = 1/2

def Initialize(stream_images : bool):
    global stream_frames
    stream_frames = stream_images

    initialize_camera()
    load_model()
   
    print('initilizing NeuralNet, stream_images: ', stream_images)
    if stream_images:
        ImageStreamer.initialize()
    
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
   
def convert_to_grayscale_one_channel(image):
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return np.reshape(grayscale, (input_image_size[1], input_image_size[0], 1))

def convert_to_grayscale_three_channel(image):
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayscale = np.reshape(grayscale, (input_image_size[1], input_image_size[0], 1))
    return np.repeat(grayscale, 3, axis=2)

# crop the image. This means removing the upper part of the image, width stays the same
def crop_image(image):
    return image[int(BASE_IMG_HEIGHT * img_height_crop_factor):BASE_IMG_HEIGHT, 0:BASE_IMG_WIDTH]

def encode_decode_image(frame):
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    _, encoded_frame = cv2.imencode('.jpg', frame, encode_param)
    processed_frame = cv2.imdecode(encoded_frame, cv2.IMREAD_COLOR)
    return processed_frame

def increase_contrast(image):
    return 1.4 * image

def predict():
    _, frame = camera.read()    

    # preprocess input
    processed_frame = encode_decode_image(frame)
    cropped_frame = crop_image(processed_frame)
    
    if stream_frames:
        ImageStreamer.send_single_frame(cropped_frame)
    
    image = cv2.resize(cropped_frame, input_image_size)
    image = convert_to_grayscale_three_channel(image)
    image = np.expand_dims(image, axis=0)

    outcomes = ['forwards', 'right', 'left']
    predictions = model.predict(image)
    prediction = outcomes[np.argmax(predictions)]

    return prediction
