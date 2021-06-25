"""
选取合适的截断阈值
"""

import os

from tqdm import tqdm
import SimpleITK as sitk

import sys
sys.path.append(os.path.split(sys.path[0])[0])

train_ct_path = r'E:\02_outputs\01_papers\02_datasets\VerSe 2019\training_data\\'
train_seg_path = r'E:\02_outputs\01_papers\02_datasets\VerSe 2019\training_data\\'
upper = 1000
lower = -1000
num_point = 0.0
num_inlier = 0.0

for file in tqdm(os.listdir(train_ct_path)):
    if '_seg.nii.gz' in file:
        ct = sitk.ReadImage(os.path.join(train_ct_path, file.replace('_seg.nii.gz', '.nii.gz')), sitk.sitkInt16)
        ct_array = sitk.GetArrayFromImage(ct)

        seg = sitk.ReadImage(os.path.join(train_seg_path, file), sitk.sitkUInt8)
        seg_array = sitk.GetArrayFromImage(seg)

        liver_roi = ct_array[seg_array > 0]
        inliers = ((liver_roi < upper) * (liver_roi > lower)).astype(int).sum()

        print('\n'+file)

        print('{:.4}%'.format(inliers / liver_roi.shape[0] * 100))
        print('------------')

        num_point += liver_roi.shape[0]
        num_inlier += inliers

print(num_inlier / num_point)

# -200 到 200 的阈值对于肝脏：训练集99.49%， 测试集99..0%
# -200 到 200 的阈值对于肿瘤：训练集99.95%， 测试集99.45%
