import os
import shutil
import sys
import argparse

parser = argparse.ArgumentParser(description='This script automatically sorts all the _synced datasets in the "images" folder regarding to their '+
                                 'labels. It automatically creates a new folder "per_label" in the "images" folder and sorts the images into subfolders'+
                                 ' called "forwards", "right" and "left".')
parser.parse_args()

def extract_label_from_imagename(filename):
    if filename == 'invalid':
        return 'delete'
    filename_without_extension = filename[:-4]
    tokens = filename_without_extension.split('_')
    label = tokens[len(tokens) - 1]
    return label

DATASETS_PATH = os.path.abspath('./images/')
PATH_RIGHT = os.path.abspath('./images/per_label/right/')
PATH_LEFT = os.path.abspath('./images/per_label/left/')
PATH_FORWARDS = os.path.abspath('./images/per_label/forwards/')

if os.path.exists(PATH_RIGHT):
    shutil.rmtree(PATH_RIGHT)
if os.path.exists(PATH_LEFT):
    shutil.rmtree(PATH_LEFT)
if os.path.exists(PATH_FORWARDS):
    shutil.rmtree(PATH_FORWARDS)

os.makedirs(PATH_RIGHT)
os.makedirs(PATH_LEFT)
os.makedirs(PATH_FORWARDS)

datasets = os.listdir(DATASETS_PATH)

# remove all datasets, which are not the synced ones
datasets_to_remove = []
for dataset in datasets:
    if not '_synced' in dataset:
        datasets_to_remove.append(dataset)

for dataset_to_remove in datasets_to_remove:
    datasets.remove(dataset_to_remove)

print('Found following datasets to sort: {}'.format(datasets))
for dataset in datasets:
    print('Now sorting dataset: {}'.format(dataset))
    dataset_path = os.path.join(DATASETS_PATH, dataset)
    dataset_files = os.listdir(dataset_path)
    for fileindex in range(len(dataset_files)):
        sys.stdout.write("\rProgress %i %%" % ((fileindex + 1) * 100 / len(dataset_files)))
        sys.stdout.flush()
        file = dataset_files[fileindex]
        label = extract_label_from_imagename(file)
        filepath = os.path.join(dataset_path, file)
        if label == 'forwards':
            dest_path = os.path.join(PATH_FORWARDS, file)
            shutil.copyfile(filepath, dest_path)
        elif label == 'right':
            dest_path = os.path.join(PATH_RIGHT, file)
            shutil.copyfile(filepath, dest_path)
        elif label == 'left':
            dest_path = os.path.join(PATH_LEFT, file)
            shutil.copyfile(filepath, dest_path)
    print()