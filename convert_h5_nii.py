import cv2
import numpy as np
import nibabel as nib
import skimage.io as io
import h5py
import os
import matplotlib.pyplot as plt

# Read a path where are the nii.gz files in.
def get_niilist(path):
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.nii.gz')]

# Define the path and a numpy array to save data
# H: height of the nii slice
# W: width of the nii slice
# D: depth of the nii slice
path_list = get_niilist('/path/to/the/.nii.gz/files')
num = len(path_list)
nii_2_array = np.empty((num, H, W, D))

# load nii data
for i in range(num):
    print('reading: ', path_list[i])
    data = nib.load(path_list[i])
    data_array = data.get_fdata()
    nii_2_array[i] = data_array
print(nii_2_array.shape)

# Create .h5 dataset which named test.h5 in path
# 'w' can write;
# 'r' read only
f = h5py.File('/path/to/the/*.h5', 'w')
label = f.create_dataset(name='label', data=nii_2_array)

# check key and value in .h5 file
# for key in f.keys():
#     print(f[key].shape)
#     print(f[key].value)
#     print(f[key].dtype)
# print(label.shape)

# Convert .h5 file to numpy array
# put different key and value in different array
nii_dataset = h5py.File('/path/to/the/*.h5', 'r')
h5_2_array = np.array(nii_dataset["label"][:])
print(h5_2_array.shape[0])


# Save numpy array to .nii files
for i in range(h5_2_array.shape[0]):
    new_array = nib.Nifti1Image(h5_2_array[i], np.eye(4))
    nib.save(new_array, str(i) + '.nii.gz')

