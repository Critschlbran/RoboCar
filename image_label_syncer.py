# idea: read image path and shift amount from cmd
# then fill the "stop" images with the next coming event label "forward", "left" or "right"
# then shift everything according to the shift amount
# create text file in sync directory specifying shift amount and how many files have been deleted at the end
import argparse
import os
import shutil

def extract_label_from_imagename(filename):
    if filename == 'invalid':
        return 'delete'
    filename_without_extension = filename[:-4]
    tokens = filename_without_extension.split('_')
    label = tokens[len(tokens) - 1]
    return label

def find_next_valid_label(files, start_index):
    for i in range(start_index, len(files)):
        filename = files[i]
        if not 'stop' in filename:
            return extract_label_from_imagename(filename)
    return 'delete'

def replace_stop_label_with_new_label(original_filename, new_label):
    new_name = original_filename.replace('stop', new_label)
    return new_name

def cleanup_file_list(files):
    for fileindex in range(0, len(files)):
        filename = files[fileindex]
        extension = filename[len(filename) - 3:]
        if not (extension == 'jpg'):
            files.remove(filename)
    return files

parser = argparse.ArgumentParser(description='Synchronize Labels and Images.')
parser.add_argument('--path', required=True, nargs=1, help='Path to the folder with the dataset.')
parser.add_argument('--shamt', required=True, nargs=1, type=int, help='Amount of shifts to apply to the labels. A positive number indicates a left shift.')
args = parser.parse_args()

shift_amount = args.shamt[0]
path_to_dataset = os.path.abspath(args.path[0])
dataset_folder_name = os.path.basename(path_to_dataset)
synced_dataset_path = path_to_dataset + "_synced"

# create new directory for the synced 
if os.path.exists(synced_dataset_path):
    shutil.rmtree(synced_dataset_path)

print("Creating a copy of the dataset...")
shutil.copytree(path_to_dataset, synced_dataset_path)
print("Done.")

print("Gathering file information...")
files = os.listdir(synced_dataset_path)
files = cleanup_file_list(files)
print("Done.")

# fix the "stop" labels
print("Renaming files to eliminate \'stop\' labels...")
for fileindex in range(0, len(files)):
    if fileindex%100 == 0:
        print(f"Progress: File {fileindex}/{len(files)}")
    
    filename = files[fileindex]
    if 'stop' in filename:
        new_label = find_next_valid_label(files, fileindex + 1)
        new_filename = replace_stop_label_with_new_label(filename, new_label)
        files[fileindex] = new_filename
        if 'delete' in new_filename:
            os.remove(synced_dataset_path + "\\" + filename)
            files.remove(new_filename)
        else:
            os.rename(synced_dataset_path + "\\" + filename, synced_dataset_path + "\\" + new_filename)
       

        
# shift the labels
print("Shifting labels...")
fileindex_range = range(0, len(files))
if shift_amount < 0:    # if a right shift should be performed, iterate the files in reverse order
    fileindex_range = range(len(files) - 1, -1, -1)
    
for fileindex in fileindex_range:
    if fileindex%100 == 0:
        print(f"Progress: File {fileindex}/{len(files)}")
    
    filename = files[fileindex]
    file_with_new_label = 'invalid'
    if fileindex + shift_amount < len(files) and fileindex + shift_amount >= 0:
        file_with_new_label = files[fileindex + shift_amount]
    
    current_label = extract_label_from_imagename(filename)
    new_label = extract_label_from_imagename(file_with_new_label)
    
    new_filename = filename.replace(current_label, new_label)
    
    if 'delete' in new_filename:
        #os.remove(synced_dataset_path + "\\" + filename)
        print("delete in new filename")
        os.rename(synced_dataset_path + "\\" + filename, synced_dataset_path + "\\" + new_filename)
    else:
        os.rename(synced_dataset_path + "\\" + filename, synced_dataset_path + "\\" + new_filename)
    