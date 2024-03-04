import cv2
import os
import numpy
import sys

def extract_label_from_imagename(filename):
    filename_without_extension = filename[:-4]
    tokens = filename_without_extension.split('_')
    label = tokens[len(tokens) - 1]
    return label

def convert_label_to_numeric_array(label):
    if label == "forwards":
        return [1, 0, 0]
    elif label == "right":
        return [0, 1, 0]
    elif label == "left":
        return [0, 0, 1]

def load_dataset(path_to_dataset :str, change_contrast : bool, image_size = (320, 240)):
    images = os.listdir(path_to_dataset)

    loaded_images = []
    loaded_labels = []

    print(f"Loading {len(images)} images and labels. This might take a while, please wait...")

    progress = 0
    for image_index in range(len(images)):
        
        new_progress = int((image_index + 1) * 100 / len(images))
        if new_progress > progress:
            sys.stdout.write("\rProgress %i %%" % ((image_index + 1) * 100 / len(images)))
            sys.stdout.flush()
        progress = new_progress

        image = images[image_index]
        full_image_path = os.path.join(path_to_dataset, image)
        label = extract_label_from_imagename(image)
        loaded_image = cv2.imread(full_image_path)
        resized_image = cv2.resize(loaded_image, image_size)
        if change_contrast:
            image_with_increased_contrast = increase_contrast(resized_image)
            loaded_images.append(image_with_increased_contrast)
        else:
            loaded_images.append(resized_image)

        loaded_labels.append(convert_label_to_numeric_array(label))

    images_numpy_array = numpy.array(loaded_images)
    labels_numpy_array = numpy.array(loaded_labels)

    print(f'\nLoaded {len(loaded_images)} images and {len(loaded_labels)} labels from directory {path_to_dataset}')
    print(f'Loaded images have shape {images_numpy_array[0].shape}.')

    return labels_numpy_array, images_numpy_array


def increase_contrast(image):
    return numpy.clip(1.4 * image, 0, 255).astype(numpy.uint8)