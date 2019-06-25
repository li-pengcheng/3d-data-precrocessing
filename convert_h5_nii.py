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
path_list = get_niilist('/data/lipengcheng/projects/pycharm/u3d/data/gt')
num = len(path_list)
nii_2_array = np.empty((num, 240, 240, 155))

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
f = h5py.File('/data/lipengcheng/projects/pycharm/u3d/data/gt/test.h5', 'w')
label = f.create_dataset(name='label', data=nii_2_array)

# check key and value in .h5 file
# for key in f.keys():
#     print(f[key].shape)
#     print(f[key].value)
#     print(f[key].dtype)
# print(label.shape)

# Convert .h5 file to numpy array
# put different key and value in different array
nii_dataset = h5py.File('/data/lipengcheng/projects/pycharm/u3d/data/gt/test.h5', 'r')
h5_2_array = np.array(nii_dataset["label"][:])
print(h5_2_array.shape[0])


# Save numpy array to .nii files
for i in range(h5_2_array.shape[0]):
    new_array = nib.Nifti1Image(h5_2_array[i], np.eye(4))
    nib.save(new_array, str(i) + '.nii.gz')


# ****************************************************************************************************
#   some test code, don't need read.
# ****************************************************************************************************
# f = h5py.File('/data/lipengcheng/projects/pycharm/u3d/resources/random_label4D.h5','r')
# # dset1 = f.create_dataset(name='dset1', shape=(10,), dtype='i')
# # dset12 = f.create_dataset(name='dset12', shape=(10,), dtype='i')
# for key in f.keys():
#     print(f[key].name)
#     print(f[key].shape)
#     print(f[key].value)

# path = "/data/lipengcheng/projects/pycharm/u3d/data/train/Brats18_2013_2_1_t1.nii.gz"
# img = nib.load(path)
# img_arr = img.get_fdata()
# print(img_arr.shape)
# print(img_arr)
# print(type(img_arr))

#
# def get_niilist(path):
#     return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.nii.gz')]
#
# # train_list = get_niilist("/data/lipengcheng/projects/pycharm/u3d/data/img")
# train_label_list = get_niilist("/data/lipengcheng/projects/pycharm/u3d/data/gt")
# # # print(train_list)
# depth = len(train_label_list)
# # #data = np.empty((depth,240,240,155))
# gt = np.empty((depth,240,240,155))
# #
# for i in range(depth):
#     #print(train_list[i])
#     print(train_label_list[i])
#     #img = nib.load(train_list[i])
#     label = nib.load(train_label_list[i])
#     print(label.get_data_dtype())
#     #img_arr = img.get_fdata()
#     label_arr = label.get_fdata()
#     # print(img_arr)
#     # print(img_arr.dtype)
#     # print(type(img_arr))
#     # data[i] = img_arr / 255.0  #CBCT should not be divive 255.0
#     gt[i] = label_arr
# print(gt.shape)
#
#
# f = h5py.File('/data/lipengcheng/projects/pycharm/u3d/resources/test.h5','w')
# # raw = f.create_dataset(name='raw', data=data)
# # label = f.create_dataset(name='label', data=gt)
# label = f.create_dataset(name='label', data=gt)
# for key in f.keys():
#     print(f[key].name)
#     print(f[key].shape)
#     #print(f[key].value)
# array = f[key].value
# a = np.array(array)
# print(a.shape)
# img = os.path.join('/data/lipengcheng/projects/pycharm/u3d/data/gt/Brats18_2013_2_1_seg.nii.gz')
# func = nib.load(img)
# ni_img = nib.Nifti1Image(a,func.affine)
# nib.save(ni_img,'output.nii.gz')