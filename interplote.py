import numpy as np
import SimpleITK as sitk
import os

def resize_image_itk(itkimage, newSpacing, resamplemethod=sitk.sitkNearestNeighbor):
    """
    image resize withe sitk resampleImageFilter
    :param itkimage:
    :param newSpacing:such as [1,1,1]
    :param resamplemethod:
    :return:
    """
    newSpacing = np.array(newSpacing, float)
    originSpcaing = itkimage.GetSpacing()
    resampler = sitk.ResampleImageFilter()
    originSize = itkimage.GetSize()
    factor = newSpacing / originSpcaing
    newSize = originSize / factor
    newSize = newSize.astype(np.int)
    resampler.SetReferenceImage(itkimage)  # 将输出的大小、原点、间距和方向设置为itkimage
    resampler.SetOutputSpacing(newSpacing.tolist())  # 设置输出图像间距
    resampler.SetSize(newSize.tolist())  # 设置输出图像大小
    resampler.SetTransform(sitk.Transform(3, sitk.sitkIdentity))
    resampler.SetInterpolator(resamplemethod)
    itkimgResampled = resampler.Execute(itkimage)
    return itkimgResampled

if __name__=="__main__":
    # path = r'E:\03_Datasets\Tooth\CBCT\Raw\3\nii\\'
    # savedir = r'C:\Users\lpc\Desktop\roi_ct\\'
    # for file in os.listdir(path):
    #     img = sitk.ReadImage(path + file)
    #     re_img = resize_image_itk(img,[0.4,0.4,0.4])
    #     sitk.WriteImage(re_img, savedir + file)
    path = r'D:\CBCT\single\020\\'
    img = sitk.ReadImage(path+'123.dcm')
    img_arr = sitk.GetArrayFromImage(img)
    img_new = sitk.GetImageFromArray(img_arr)
    sitk.WriteImage(img_new, path+'//123.nii.gz')
    # print(img_arr.shape)