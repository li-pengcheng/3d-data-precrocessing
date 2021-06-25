# from skimage import measure, morphology
# import SimpleITK as sitk
# import numpy as np
#
# img = sitk.ReadImage(r'C:\Users\lpc\Desktop\test_instance.nii.gz')
# img_arr = sitk.GetArrayFromImage(img)
# img_1 = np.where(img_arr==1,1,0)
# [tooth_res, num] = measure.label(img_1, connectivity=1, return_num=True)
# print(num)
# region = measure.regionprops(tooth_res)
# box=[]
# for i in range(num):
#     box.append(region[i].area)
#
# tooth = sitk.GetImageFromArray(tooth_res.astype(np.uint8))
# # sitk.WriteImage(tooth, r'C:\Users\lpc\Desktop\test_1.nii.gz')
#
#
#
# # for i in range(1, 9):
# #     img_single_class = np.where(img_arr == i, 1, 0)
# #     labels = measure.label(img_single_class, connectivity=1)
# #
# #     for j in range(labels.max()):
# #         for region in measure.regionprops(labels):  # 循环得到每一个连通区域属性
# #             # 忽略小区域
# #             if region.area < 100:
# #                 continue
# #             label = np.where(labels == j + 1, j + 1 , 0)
# #             label_new = sitk.GetImageFromArray(label)
# #             sitk.WriteImage(label_new, r'C:\Users\lpc\Desktop\test\\' + str(i) + '_' + str(j+1) + '.nii.gz')
#
# def connected_component(image):
#     # 标记输入的3D图像
#     label, num = measure.label(image, connectivity=1, return_num=True)
#     if num < 1:
#         return image
#
#     # 获取对应的region对象
#     region = measure.regionprops(label)
#     # 获取每一块区域面积并排序
#     num_list = [i for i in range(1, num + 1)]
#     area_list = [region[i - 1].area for i in num_list]
#     num_list_sorted = sorted(num_list, key=lambda x: area_list[x - 1])[::-1]
#     # 去除面积较小的连通域
#     if len(num_list_sorted) > 4:
#         # for i in range(3, len(num_list_sorted)):
#         for i in num_list_sorted[4:]:
#             # label[label==i] = 0
#             label[region[i - 1].slice][region[i - 1].image] = 0
#         num_list_sorted = num_list_sorted[:4]
#     return label
#
# img_1 = np.where(img_arr==1,1,0)
# label = connected_component(img_1).astype(np.uint8)
# label_new = sitk.GetImageFromArray(label)
#
#
# # 将81234567转化为87654321
# # img_arr[img_arr==8] = 100
# # img_arr[img_arr==0] = 200
# # img_arr = abs(img_arr-8)
# # img_arr[img_arr==192] = 0
# # img_arr[img_arr==92] = 8
# # # label = connected_component(img_arr).astype(np.int8)
# # label_new = sitk.GetImageFromArray(img_arr)
# sitk.WriteImage(label_new, r'C:\Users\lpc\Desktop\test_instance.nii.gz')
#
#
from skimage import measure, morphology
import SimpleITK as sitk


img = sitk.ReadImage(r'C:\Users\lpc\Desktop\segmentation-1001832865.nii.gz')
filter = sitk.BinaryErodeImageFilter()
filter.SetKernelRadius(1)
filter.SetForegroundValue(2)
eroded = filter.Execute ( img )
sitk.WriteImage(eroded, r'C:\Users\lpc\Desktop\test_instance.nii.gz')

