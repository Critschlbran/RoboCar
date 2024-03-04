import cv2
import argparse
import os
import dataset_utils

parser = argparse.ArgumentParser(description='Mirrors and copys the images with left/right label.')
parser.add_argument('--path', required=True, nargs=1, type=str, help='Path to the folder containing the images.')

args = parser.parse_args()

path = args.path[0]

images = os.listdir(os.path.abspath(path))

counter_labels = {'left': 'right',
                'right': 'left'}

for image in images:
    if 'forwards' in image:
        continue

    image_label = dataset_utils.extract_label_from_imagename(image)
    new_filename = image.replace(image_label, counter_labels[image_label])

    loaded_image = cv2.imread(os.path.join(path, image))

    # flipCode 1 means flip horizontally
    flipped_image = cv2.flip(loaded_image, 1)

    cv2.imwrite(os.path.join(path, new_filename), flipped_image)




