"""
读取具有dicom数据的文件夹并将其保存为nii
"""
import SimpleITK as sitk
import numpy as np
import os
import shutil

def file_name_walk(file_dir):
    i = 1
    for root, dirs, files in os.walk(file_dir):
        # print("root", root)  # 当前目录路径
        # print("dirs", dirs)  # 当前路径下所有子目录
        # print("files", files)  # 当前路径下所有非目录子文件
        if files: #判断是否为空
            if 'dcm' in files[0]:
                print(root)  # 有dcm的文件夹
                # print(dirs)  # 有dcm的文件夹
                # print(files) # dcm文件
                if len(files)>50:
                    target_path = r'D:\CT\series\\' + str(i).zfill(3) + '\\'
                else:
                    target_path = r'D:\CT\single\\' + str(i).zfill(3) + '\\'
                # if not os.path.exists(target_path):
                #     # 如果目标路径不存在原文件夹的话就创建
                #     os.makedirs(target_path)
                shutil.copytree(root, target_path)
                print('copy dir finished!')

                # reader = sitk.ImageSeriesReader()
                # img_names = reader.GetGDCMSeriesFileNames(root)
                # reader.SetFileNames(img_names)
                # image = reader.Execute()
                # print(image.GetSize())
                # image_array = sitk.GetArrayFromImage(image)  # z, y, x
                # # print(image_array.shape)
                # image = sitk.GetImageFromArray(image_array, sitk.sitkInt16)
                # sitk.WriteImage(image, save_dir + str(i).zfill(3) + '.nii.gz')
                i = i + 1


if __name__ == "__main__":

    img_path = r'E:\03_Datasets\Tooth\CBCT\Raw\3\cbct1'
    save_dir = r'E:\03_Datasets\Tooth\CBCT\Raw\3\nii\\'
    file_name_walk(img_path)