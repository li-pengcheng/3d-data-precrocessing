import cv2
import numpy as np
import SimpleITK as sitk


dcm_file = r'G:\data\3Dircadb\3Dircadb1.3\PATIENT_DICOM\image_137'
dcm_liver = r'G:\data\3Dircadb\3Dircadb1.3\MASKS_DICOM\liver\image_137'
dcm_tumor = r'G:\data\3Dircadb\3Dircadb1.3\MASKS_DICOM\livertumor\image_137'


def drawContour():

    image = sitk.ReadImage(dcm_file)
    image_array = sitk.GetArrayFromImage(image)
    image_array = np.squeeze(image_array)
    image_array = image_array.astype(np.float32)
	# windowing 操作
    # min:-200, max:200
    # img = (img-min)/(max - min)
    image_array = (image_array - (-200)) / 400.0
    image_array[image_array > 1] = 1.0
    image_array[image_array < 0] = 0.0
    # 不必须转化为0-255

    # 若不转化为彩色，那么最后画出来的contour也只能是灰度的
    image_array = cv2.cvtColor(image_array, cv2.COLOR_GRAY2BGR)

    liver = sitk.ReadImage(dcm_liver)
    liver_array = sitk.GetArrayFromImage(liver)
    liver_array = np.squeeze(liver_array)
    # liver_array *= 255 不必须

    tumor = sitk.ReadImage(dcm_tumor)
    tumor_array = sitk.GetArrayFromImage(tumor)
    tumor_array = np.squeeze(tumor_array)
    # tumor_array *= 255 不必须

    # findContours 必须目标是white，背景是black (0,1 和 0,255 都可以)
    # py3 只返回2个参数，而非之前的3个
    contours, hierarchy = cv2.findContours(
        liver_array, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contours2, hierarchy2 = cv2.findContours(
        tumor_array, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnt = contours[0]
    # drawContours 直接改变原图
    # 第三个参数 index
    # 第四个参数color: BGR
    # 两种不同的方式指明画哪个contour
    cv2.drawContours(image_array, [cnt], 0, (0, 0, 255), 1)
    cv2.drawContours(image_array, contours2, -1,
                     (255, 0, 0), 1)  # index=-1表示画所有的contour
    cv2.imshow("liver_contour", image_array)
    cv2.waitKey()


drawContour()

