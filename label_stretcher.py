import argparse
import os

def extract_label_from_imagename(filename):
    if filename == 'invalid':
        return 'delete'
    filename_without_extension = filename[:-4]
    tokens = filename_without_extension.split('_')
    label = tokens[len(tokens) - 1]
    return label

parser = argparse.ArgumentParser(description='A small script to increase the amount of images a label block covers. ' + 
                                 'Example: If image X has the label "forwards", X+1 as well as X+2 have "right" and' + 
                                 'the stretch amount is 1, X keeps "forwards", X+1 gets "forwards" now and X+2 keeps "right.')
parser.add_argument('--path', type=str, required=True, help='Path to the dataset whose labels should be stretched.')
parser.add_argument('--stretch_amount', type=int, required=True, help='Amount to which the labels should be stretched. Only positive values are allowed.')
args = parser.parse_args()


stretch_amount = args.stretch_amount
dataset_path = os.path.abspath(args.path)

# check the validity of the arguments
if stretch_amount < 0 or not os.path.exists(dataset_path) or not dataset_path.endswith('_synced'):
    print('Program requirements not met. Requirements are:')
    print('Stretch amount has to be greater than or equal to zero.')
    print('Path to dataset has to exist.')
    print('Given dataset has to be already synced.')

files = os.listdir(dataset_path)

prev_label = extract_label_from_imagename(files[0])
currently_stretched = 0
stretch_in_action = False

for file in files:
    current_label = extract_label_from_imagename(file)

    if current_label != prev_label and stretch_in_action == False:
        stretch_in_action = True

    if stretch_in_action:
        if currently_stretched < stretch_amount:
            currently_stretched += 1
            new_filename = file.replace(current_label, prev_label)
            os.rename(os.path.join(dataset_path, file), os.path.join(dataset_path, new_filename))
            continue
        else:
            stretch_in_action = False
            currently_stretched = 0
    prev_label = current_label