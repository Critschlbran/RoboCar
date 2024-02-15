from PIL import Image
import os
import shutil
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--path', required=True, nargs=1, type=str, help='Path to the folder containing the images which should be cropped.')
parser.add_argument('--crop_amount', required=False, nargs=1, type=int, default=[120], help='Amount of pixels to crop the images vertically.')

args = parser.parse_args()
path = args.path[0]
crop_amount = args.crop_amount[0]

images_base_path = os.path.abspath(path)
save_path = os.path.normpath(os.path.join(images_base_path, '..', os.path.basename(images_base_path) + '_cropped'))

print(f'Loading images from {images_base_path}')
print(f'Saving cropped images to {save_path}')

if os.path.exists(save_path):
    shutil.rmtree(save_path)

os.mkdir(save_path)

images = os.listdir(images_base_path)

progress = 0
for fileindex in range(len(images)):

    new_progress = int((fileindex + 1) * 100 / len(images))
    if new_progress > progress:
        sys.stdout.write("\rProgress %i %%" % ((fileindex + 1) * 100 / len(images)))
        sys.stdout.flush()
    progress = new_progress

    file = images[fileindex]
    image = Image.open(os.path.join(images_base_path, file))
    
    # crops image to be 320x(240 - crop_amount)
    cropped_image = image.crop((0, crop_amount, 320, 240))
    cropped_image.save(os.path.join(save_path, file))

print() # newline
