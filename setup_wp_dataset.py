from pathlib import Path
from posixpath import curdir
from PIL import Image
import os
import glob
import shutil
import sys
from distutils.dir_util import copy_tree

import PIL


def run():
    curr_dir = os.curdir
    dataset_dir = os.path.join(curdir, 'WiderPerson/')

    if not os.path.exists(dataset_dir):
        print('WiderPerson/ directory does not exist.\nExiting...\n')
        sys.exit(1)

    # Path Initialization
    anno_dir = os.path.join(dataset_dir, 'Annotations/')
    img_dir = os.path.join(dataset_dir, 'Images/')
    test_path = os.path.join(dataset_dir, 'test.txt')
    train_path = os.path.join(dataset_dir, 'train.txt')
    val_path = os.path.join(dataset_dir, 'val.txt')

    data_dir = os.path.join(curr_dir, 'data/')
    data_custom_dir = os.path.join(data_dir, 'custom/')
    data_custom_img_dir = os.path.join(data_custom_dir, 'images/')
    data_custom_labels_dir = os.path.join(data_custom_dir, 'labels/')

    custom_train_path = os.path.join(data_custom_dir, 'train.txt')
    custom_valid_path = os.path.join(data_custom_dir, 'valid.txt')
    custom_test_path = os.path.join(data_custom_dir, 'test.txt')

    # Copy Images
    copy_tree(img_dir, data_custom_img_dir)

    # Write Classes
    write_class_names(data_custom_dir)

    # Convert Annotations, Taking Image Size into Account
    anno_list = glob.glob(anno_dir + '*')
    for filename in anno_list:
        write_annotations(filename, data_custom_labels_dir,
                          data_custom_img_dir)

    # Write Test Train Validation
    write_test_train_validation(test_path, train_path, val_path,
                                custom_test_path, custom_train_path, custom_valid_path, data_custom_img_dir)


def write_class_names(data_custom_dir):
    with open(os.path.join(data_custom_dir, 'classes.names'), 'w') as f:
        f.writelines(['pedestrians\n', 'riders\n',
                     'partially-visible persons\n', 'ignore regions\n', 'crowd\n'])


def write_annotations(filename, data_custom_labels_dir, data_custom_img_dir):
    file_basename_jpg = os.path.basename(filename)[:-4]
    file_basename_txt = os.path.basename(filename)[:-7] + 'txt'
    w, h = Image.open(os.path.join(
        data_custom_img_dir, file_basename_jpg)).size
    anno_lines = []
    with open(filename, 'r') as f:
        anno_lines = f.readlines()
    anno_lines = anno_lines[1:]  # First line is total anno count
    anno_write_lines = []
    for line in anno_lines:
        wp_label, x1, y1, x2, y2 = line.split()
        wp_label = int(wp_label)
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)
        yolo_label = str(wp_label-1)
        xc = str((x2+x1)/(2*w))
        yc = str((y2+y1)/(2*h))
        yolo_width = str((x2-x1)/w)
        yolo_height = str((y2-y1)/h)
        yolo_line = " ".join(
            [yolo_label, xc, yc, yolo_width, yolo_height, '\n'])
        anno_write_lines.append(yolo_line)

    with open(os.path.join(data_custom_labels_dir, file_basename_txt), 'w') as f:
        f.writelines(anno_write_lines)


def write_test_train_validation(test_path, train_path, val_path,
                                custom_test_path, custom_train_path, custom_valid_path, data_custom_img_dir):
    # Test
    test_path_list = []
    with open(test_path, 'r') as f:
        test_path_list = f.readlines()
    test_path_list = [x[:-1]+'.jpg\n' if x[-1]=='\n' else x+'.jpg\n' for x in test_path_list]
    test_path_list = [os.path.join(data_custom_img_dir, x)
                      for x in test_path_list]
    with open(custom_test_path, 'w') as f:
        f.writelines(test_path_list)

    # Train
    train_path_list = []
    with open(train_path, 'r') as f:
        train_path_list = f.readlines()
    train_path_list = [x[:-1]+'.jpg\n' if x[-1]=='\n' else x+'.jpg\n' for x in train_path_list]
    train_path_list = [os.path.join(data_custom_img_dir, x)
                       for x in train_path_list]
    with open(custom_train_path, 'w') as f:
        f.writelines(train_path_list)

    # Validation
    valid_path_list = []
    with open(val_path, 'r') as f:
        valid_path_list = f.readlines()
    valid_path_list = [x[:-1]+'.jpg\n' if x[-1]=='\n' else x+'.jpg\n' for x in valid_path_list]
    valid_path_list = [os.path.join(data_custom_img_dir, x)
                       for x in valid_path_list]
    with open(custom_valid_path, 'w') as f:
        f.writelines(valid_path_list)


if __name__ == '__main__':
    run()
