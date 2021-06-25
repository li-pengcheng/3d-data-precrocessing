from glob import glob
from tqdm import tqdm
import h5py
import SimpleITK as sitk
import os
import shutil
import numpy as np
from scipy.ndimage import distance_transform_edt as distance
from skimage import segmentation as skimage_seg
import torch

def normalize(data):
    volume = data
    pixels = volume[volume > 0]
    mean = pixels.mean()
    std  = pixels.std()
    out = (volume - mean)/std
    out_random = np.zeros(volume.shape)
    out[volume == 0] = out_random[volume == 0]
    return out


def compute_sdf(img_gt, out_shape):
    """
    compute the signed distance map of binary mask
    input: segmentation, shape = (class, x, y, z)
    output: the Signed Distance Map (SDM)
    sdf(x) = 0; x in segmentation boundary
             -inf|x-y|; x in segmentation
             +inf|x-y|; x out of segmentation
    normalize sdf to [-1,1]
    """

    img_gt = img_gt.astype(np.uint8)
    normalized_sdf = np.zeros(out_shape)

    for c in range(out_shape[0]):
        img_gt_class = np.where(img_gt==c, 1, 0)
        posmask = img_gt_class.astype(np.bool)
        if posmask.any():
            negmask = ~posmask
            posdis = distance(posmask)
            negdis = distance(negmask)
            boundary = skimage_seg.find_boundaries(posmask, mode='inner').astype(np.uint8)
            sdf = (negdis - np.min(negdis)) / (np.max(negdis) - np.min(negdis)) - (posdis - np.min(posdis)) / (
                        np.max(posdis) - np.min(posdis))
            sdf[boundary == 1] = 0
            normalized_sdf[c] = sdf
            # assert np.min(sdf) == -1.0, print(np.min(posdis), np.max(posdis), np.min(negdis), np.max(negdis))
            # assert np.max(sdf) == 1.0, print(np.min(posdis), np.min(negdis), np.max(posdis), np.max(negdis))


    return normalized_sdf

def covert_h5():
    root_path = '/home/crop/'
    ct_path = root_path + '/ct/'
    listt = sorted(glob(ct_path + '*.nii.gz'))
    h5_savepath = root_path + '/h5/'
    if not os.path.exists(h5_savepath):
        os.mkdir(h5_savepath)
    for item in tqdm(listt):
        image = sitk.ReadImage(item)
        image_arr = sitk.GetArrayFromImage(image)
        # label = sitk.ReadImage(item.replace('ct\\volume', 'seg\\segmentation'))

        label = sitk.ReadImage(item.replace('ct/volume', 'seg/segmentation'))
        label_arr = sitk.GetArrayFromImage(label).astype(np.uint8)
        #
        # label_arr[label_arr > 40] = 4
        # label_arr[label_arr > 30] = 3
        # label_arr[label_arr > 20] = 2
        # label_arr[label_arr > 10] = 1

        # label_batch_onehot = torch.zeros_like(torch.zeros([9,128,128,128]))  # output shape: (batch, classes, w, h, d)
        # label_batch_onehot.scatter_(1, torch.from_numpy(label_arr).long().unsqueeze(0), 0)  # label_batch shape (batch, w, h, d)
        # gt_dis = compute_sdf(label_arr, label_batch_onehot.shape)

        # 归一化
        # image_arr = normalize(image_arr)
        # image_arr = image_arr.astype(np.float32)
        image_arr = (image_arr - np.min(image_arr)) / (np.max(image_arr) - np.min(image_arr))
        image_arr = image_arr.astype(np.float32)

        # ## add sobel edge map
        # data_nii = label
        # origin = data_nii.GetOrigin()
        # spacing = data_nii.GetSpacing()
        # direction = data_nii.GetDirection()
        #
        # # change data type before edge detection
        # data_float_nii = sitk.Cast(data_nii, sitk.sitkFloat32)
        #
        # sobel_op = sitk.SobelEdgeDetectionImageFilter()
        # sobel_sitk = sobel_op.Execute(data_float_nii)
        # sobel_sitk = sitk.Cast(sobel_sitk, sitk.sitkInt16)
        #
        # sobel_sitk.SetOrigin(origin)
        # sobel_sitk.SetSpacing(spacing)
        # sobel_sitk.SetDirection(direction)
        #
        # # 归一化
        # sobel_arr = sitk.GetArrayFromImage(sobel_sitk)
        # sobel_arr = (sobel_arr - np.min(sobel_arr)) / (np.max(sobel_arr) - np.min(sobel_arr))
        # sobel_arr = sobel_arr.astype(np.float32)
        # sobel_arr[sobel_arr > 0] = 1

        # f = h5py.File(h5_savepath +'\\'+ item.split('.nii.gz')[0].split('\\')[-1] + '.h5', 'w')
        f = h5py.File(h5_savepath + item.split('.nii.gz')[0].split('/')[-1] + '.h5', 'w')
        f.create_dataset('image', data=image_arr, compression="gzip")
        f.create_dataset('label', data=label_arr, compression="gzip")
        # f.create_dataset('sobel', data=sobel_arr, compression="gzip")
        # f.create_dataset('sdf', data=gt_dis, compression="gzip")
        f.close()

if __name__ == '__main__':
    covert_h5()
    # import h5py
    # import SimpleITK as sitk
    # h5f = h5py.File('/home/volume-1001086638_20190828.h5')
    # img = h5f['image']
    # print(img.shape)