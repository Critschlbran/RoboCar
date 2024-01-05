import argparse
import os
import cv2

def extract_label_from_imagename(filename):
    if filename == 'invalid':
        return 'delete'
    filename_without_extension = filename[:-4]
    tokens = filename_without_extension.split('_')
    label = tokens[len(tokens) - 1]
    return label

parser = argparse.ArgumentParser(description="A script to play back a dataset.")
parser.add_argument('--framerate', required=False, type=int, default=30, nargs=1, help='Framerate which should be used for playback.')
parser.add_argument('--path', required=True, nargs=1, help='Path to the folder with the dataset.')
args = parser.parse_args()

framerate = args.framerate[0]
path_to_dataset = os.path.abspath(args.path[0])
wait_time_ms = int(1000 / framerate)

files = os.listdir(path_to_dataset)

# config for displaying the driving status on the image
font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfDrivingStatusLabel = (10,50)
fontScale              = 1
fontColor              = (255,255,255)
thickness              = 1
lineType               = 2

for file in files:
    full_filepath = path_to_dataset + "\\" + file
    image = cv2.imread(full_filepath, cv2.IMREAD_COLOR)
    label = extract_label_from_imagename(file)
    cv2.putText(image, label, bottomLeftCornerOfDrivingStatusLabel, font, fontScale, fontColor, thickness, lineType)
    cv2.imshow('image', image)
    cv2.waitKey(wait_time_ms)