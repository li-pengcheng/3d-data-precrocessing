"""
对数据进行预处理

首先将灰度值超过upper和低于lower的灰度进行截断

然后调整slice thickness，然后将slice的分辨率调整为H*W (option)

只有包含target以及target上下 expand_slice 张slice作为训练样本

最终每个样本尺寸为size*H*W
"""

import os
import shutil
import numpy as np
import SimpleITK as sitk
from time import time


upper = 2500
lower = -500

expand_slice = 5  # 轴向上向外扩张的slice数量

# 原始路径
root_path = '/home/lipengcheng/Data/instance_CBCT/train/'

ct_dir = root_path + 'ct/'
seg_dir = root_path + 'seg/'

# 保存路径
processed_path = root_path + 'processed_second_coord/'
new_ct_dir = processed_path + 'ct/'
new_seg_dir = processed_path + 'seg/'

if os.path.exists(processed_path):
    shutil.rmtree(processed_path)
os.mkdir(processed_path)
os.mkdir(new_ct_dir)
os.mkdir(new_seg_dir)

start_time = time()
for ct_file in os.listdir(ct_dir):
    if '.nii.gz' in ct_file:
        # 将CT和金标准入读内存
        print(ct_file)
        ct = sitk.ReadImage(os.path.join(ct_dir, ct_file), sitk.sitkInt16)
        ct_array = sitk.GetArrayFromImage(ct)

        seg = sitk.ReadImage(os.path.join(seg_dir, ct_file.replace('volume', 'segmentation')), sitk.sitkInt8)
        # seg = sitk.ReadImage(os.path.join(seg_dir, ct_file), sitk.sitkInt8)
        seg_array = sitk.GetArrayFromImage(seg)

        # # 将金标准中肝脏和肝肿瘤的标签融合为一个
        # seg_array[seg_array > 0] = 1
        # 不分割智齿，label 8 视为背景
        # seg_array[seg_array == 8] = 0

        # 将灰度值在阈值之外的截断掉
        ct_array[ct_array > upper] = upper
        ct_array[ct_array < lower] = lower

        seg_array[seg_array < 40] = 0

        seg_array = (seg_array%10).astype(np.uint8)

        # z-score或者归一化
        # ct_array = (ct_array - ct_array.max()) / (ct_array.max()-ct_array.min())
        # ct_array = (ct_array - ct_array.mean()) / ct_array.std()

        # # 对CT和金标准进行插值，插值之后的array依然是int类型
        # ct_array = ndimage.zoom(ct_array, (ct.GetSpacing()[-1] / slice_thickness, down_scale, down_scale), order=3)
        # seg_array = ndimage.zoom(seg_array, (ct.GetSpacing()[-1] / slice_thickness, 1, 1), order=0)

        # 找到肝脏区域开始和结束的slice，并各向外扩张
        z = np.any(seg_array, axis=(1, 2))
        start_slice_z, end_slice_z = np.where(z)[0][[0, -1]]

        # 两个方向上各扩张个slice
        if start_slice_z - expand_slice < 0:
            start_slice_z = 0
        else:
            start_slice_z -= expand_slice

        if end_slice_z + expand_slice >= seg_array.shape[0]:
            end_slice_z = seg_array.shape[0] - 1
        else:
            end_slice_z += expand_slice

        # 找到肝脏区域开始和结束的slice，并各向外扩张
        y = np.any(seg_array, axis=(0, 2))
        start_slice_y, end_slice_y = np.where(y)[0][[0, -1]]

        # 两个方向上各扩张个slice
        if start_slice_y - expand_slice < 0:
            start_slice_y = 0
        else:
            start_slice_y -= expand_slice

        if end_slice_y + expand_slice >= seg_array.shape[1]:
            end_slice_y = seg_array.shape[1] - 1
        else:
            end_slice_y += expand_slice

        # 找到肝脏区域开始和结束的slice，并各向外扩张
        x = np.any(seg_array, axis=(0, 1))
        start_slice_x, end_slice_x = np.where(x)[0][[0, -1]]

        # 两个方向上各扩张个slice
        if start_slice_x - expand_slice < 0:
            start_slice_x = 0
        else:
            start_slice_x -= expand_slice

        if end_slice_x + expand_slice >= seg_array.shape[2]:
            end_slice_x = seg_array.shape[2] - 1
        else:
            end_slice_x += expand_slice

        # # 如果这时候剩下的slice数量不足size，直接放弃，这样的数据很少
        # if end_slice - start_slice + 1 < size:
        #     print('!!!!!!!!!!!!!!!!')
        #     print(ct_file, 'too little slice')
        #     print('!!!!!!!!!!!!!!!!')
        #     continue
        #
        new_ct_array = ct_array[start_slice_z:end_slice_z, start_slice_y:end_slice_y, start_slice_x:end_slice_x]
        new_seg_array = seg_array[start_slice_z:end_slice_z, start_slice_y:end_slice_y, start_slice_x:end_slice_x]


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

        # 每处理完一个数据，打印一次已经使用的时间
        print('already use {:.3f} min'.format((time() - start_time) / 60))
        print('-----------')

