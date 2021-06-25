import SimpleITK as sitk
import numpy as np
import os
import shutil

# 原始路径
root_path = '/home/lipengcheng/Data/instance_CBCT/train/processed_second_coord/'

ct_dir = root_path + 'ct/'
seg_dir = root_path + 'seg/'

# 保存路径
processed_path = root_path + 'flip/'
new_ct_dir = processed_path + 'ct/'
new_seg_dir = processed_path + 'seg/'

if os.path.exists(processed_path):
    shutil.rmtree(processed_path)
os.mkdir(processed_path)
os.mkdir(new_ct_dir)
os.mkdir(new_seg_dir)

for ct_file in os.listdir(ct_dir):
    if '.nii.gz' in ct_file:
        # 将CT和金标准入读内存
        # print(ct_file)
        ct = sitk.ReadImage(os.path.join(ct_dir, ct_file), sitk.sitkInt16)
        ct_array = sitk.GetArrayFromImage(ct)

        seg = sitk.ReadImage(os.path.join(seg_dir, ct_file.replace('volume', 'segmentation')), sitk.sitkInt8)
        # seg = sitk.ReadImage(os.path.join(seg_dir, ct_file), sitk.sitkInt8)
        seg_array = sitk.GetArrayFromImage(seg)

        new_ct_array = np.flip(ct_array, axis=1)
        new_seg_array = np.flip(seg_array, axis=1)

        new_ct = sitk.GetImageFromArray(new_ct_array)
        new_ct.SetDirection(ct.GetDirection())
        new_ct.SetOrigin(ct.GetOrigin())
        new_ct.SetSpacing(ct.GetSpacing())

        new_seg = sitk.GetImageFromArray(new_seg_array)
        new_seg.SetDirection(ct.GetDirection())
        new_seg.SetOrigin(ct.GetOrigin())
        new_seg.SetSpacing(ct.GetSpacing())

        print('{} have {} slice'.format(ct_file, new_ct_array.shape))

        sitk.WriteImage(new_ct, os.path.join(new_ct_dir, ct_file))
        sitk.WriteImage(new_seg, os.path.join(new_seg_dir, ct_file.replace('volume','segmentation')))