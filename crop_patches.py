"""
Crop 3D数据[w,h,d]到固定尺寸
 :param:patch_size 输出的尺寸
"""
import os
import shutil
import numpy as np
import SimpleITK as sitk
import math
from time import time
from tqdm import tqdm

# 原始路径
root_path = '/home/lipengcheng/Data/instance_CBCT/train/processed_second_coord/flip/'

ct_dir = root_path + 'ct/'
seg_dir = root_path + 'seg/'

# 保存路径
processed_path = root_path + 'crop/'
new_ct_dir = processed_path + 'ct/'
new_seg_dir = processed_path + 'seg/'

if os.path.exists(processed_path):
    shutil.rmtree(processed_path)
os.mkdir(processed_path)
os.mkdir(new_ct_dir)
os.mkdir(new_seg_dir)

# crop的大小以及滑动窗口的大小
patch_size = [96, 96, 96]  #zxy
stride = [48, 48, 48]
upper = 2500
lower = -500

start_time = time()

for ct_file in tqdm(os.listdir(ct_dir)):
    if '.nii.gz' in ct_file:
        # 将CT和金标准入读内存
        print(ct_file)
        ct = sitk.ReadImage(os.path.join(ct_dir, ct_file), sitk.sitkInt16)
        ct_array = sitk.GetArrayFromImage(ct)
        # 将灰度值在阈值之外的截断掉
        ct_array[ct_array > upper] = upper
        ct_array[ct_array < lower] = lower

        seg = sitk.ReadImage(os.path.join(seg_dir, ct_file.replace('volume', 'segmentation')), sitk.sitkInt8)
        seg_array = sitk.GetArrayFromImage(seg)

        w, h, d = ct_array.shape  #zyx:dhw
        # print('image shape:', w, h, d)
        # if the size of image is less than patch_size, then padding it
        add_pad = False
        if w < patch_size[0]:
            w_pad = patch_size[0] - w
            add_pad = True
        else:
            w_pad = 0
        if h < patch_size[1]:
            h_pad = patch_size[1] - h
            add_pad = True
        else:
            h_pad = 0
        if d < patch_size[2]:
            d_pad = patch_size[2] - d
            add_pad = True
        else:
            d_pad = 0
        wl_pad, wr_pad = w_pad // 2, w_pad - w_pad // 2
        hl_pad, hr_pad = h_pad // 2, h_pad - h_pad // 2
        dl_pad, dr_pad = d_pad // 2, d_pad - d_pad // 2
        if add_pad:
            print(ct_file)
            print('image shape:', w, h, d)
            ct_array = np.pad(ct_array, [(wl_pad, wr_pad), (hl_pad, hr_pad), (dl_pad, dr_pad)], mode='constant',
                           constant_values=0)
            seg_array = np.pad(seg_array, [(wl_pad, wr_pad), (hl_pad, hr_pad), (dl_pad, dr_pad)], mode='constant',
                           constant_values=0)
            ww, hh, dd = ct_array.shape
            print('i_new shape:', ww, hh, dd)

            # sitk.WriteImage(new_ct,
            #                 new_ct_dir + ct_file.split('.')[0] + ".nii.gz")
            # sitk.WriteImage(new_seg,
            #                 new_seg_dir + ct_file.split('.')[0] + '_seg' + ".nii.gz")

        ww, hh, dd = ct_array.shape

        sx = math.ceil((ww - patch_size[0]) / stride[0]) + 1
        sy = math.ceil((hh - patch_size[1]) / stride[1]) + 1
        sz = math.ceil((dd - patch_size[2]) / stride[2]) + 1
        print("Sliding...\nx slide numbers:{}, y slide numbers:{}, z slide numbers:{}".format(sx, sy, sz))
        patch_num = 1
        for x in range(0, sx):
            xs = min(stride[0] * x, ww - patch_size[0])
            for y in range(0, sy):
                ys = min(stride[1] * y, hh - patch_size[1])
                for z in range(0, sz):
                    zs = min(stride[2] * z, dd - patch_size[2])
                    new_img_patch = ct_array[xs:xs + patch_size[0], ys:ys + patch_size[1], zs:zs + patch_size[2]]
                    new_seg_patch = seg_array[xs:xs + patch_size[0], ys:ys + patch_size[1], zs:zs + patch_size[2]]

                    new_ct = sitk.GetImageFromArray(new_img_patch.astype(np.float32))
                    new_ct.SetDirection(ct.GetDirection())
                    new_ct.SetOrigin(ct.GetOrigin())
                    new_ct.SetSpacing(ct.GetSpacing())
                    sitk.WriteImage(new_ct,
                                    new_ct_dir + ct_file.split('.')[0] + '_' + str(patch_num).zfill(2) + ".nii.gz")
                                    # new_ct_dir +'\\' + ct_file.split('.')[0] + '_' + str(patch_num).zfill(2) + ".nii.gz")

                    new_seg = sitk.GetImageFromArray(new_seg_patch.astype(np.int16))
                    new_seg.SetDirection(ct.GetDirection())
                    new_seg.SetOrigin(ct.GetOrigin())
                    new_seg.SetSpacing(ct.GetSpacing())
                    sitk.WriteImage(new_seg,
                                    new_seg_dir + ct_file.replace('volume', 'segmentation').split('.')[0]
                                    # new_seg_dir +'\\' + ct_file.replace('volume', 'segmentation').split('.')[0]
                                    + '_' + str(patch_num).zfill(2) + ".nii.gz")
                    patch_num += 1



