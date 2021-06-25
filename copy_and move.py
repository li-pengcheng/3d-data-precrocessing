# import os
# import shutil
#
#
#
# def copyfiles():
#  original_path = r"E:\03_Datasets\Tooth\CBCT\Raw\processed_one\refined"
#  premoved_path = r"E:\03_Datasets\Tooth\CBCT\Raw\processed_one\ct"
#  target_path = r"E:\03_Datasets\Tooth\CBCT\Raw\processed_one\test_ct"
#  f_list = os.listdir(original_path)
#  for fileNAME in f_list:
#      ct_name = fileNAME.replace('tooth_', 'volume-')
#      if ct_name in os.listdir(premoved_path):
#         oldname = os.path.join(premoved_path, ct_name)
#         newname = os.path.join(target_path, ct_name)
#         shutil.copyfile(oldname, newname)
#
# def copyfiles2():
#  original_path = r'E:\03_Datasets\Tooth\CBCT\Labeled\instance_seg2\\'
#  premoved_path = r'E:\03_Datasets\Tooth\CBCT\Labeled\ROI_seg2\\'
#  f_list = os.listdir(original_path)
#  for fileNAME in f_list:
#      if fileNAME in os.listdir(premoved_path):
#          os.remove(premoved_path + fileNAME)
#
# if __name__ == '__main__':
#  copyfiles2()

import os

def recursive_glob(rootdir='.', suffix=''):
    """Performs recursive glob with given suffix and rootdir
        :param rootdir is the root directory
        :param suffix is the suffix to be searched
    """
    return [os.path.join(looproot, filename)
        for looproot, _, filenames in os.walk(rootdir)
        for filename in filenames if filename.endswith(suffix)]

if __name__=='__main__':
    # path = '/home/lipengcheng/Data/complete/processed/h5/'
    path = r'D:\CBCT\\'
    dirs = sorted(os.listdir(path))
    save_list = open('D:\\' + 'dicom.txt', 'w')
    for file in dirs:
        len = os.listdir(path + file).__len__()
        if len > 50:
            save_list.write(file + ' slices: ' + str(len).zfill(3) + '\n', )
    save_list.close()