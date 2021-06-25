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
    path = '/home/lipengcheng/Data/instance_CBCT/train/processed_first_coord/crop/second2first_h5/'
    files = sorted(recursive_glob(rootdir=path,suffix='h5'))
    save_list = open(path + 'train.txt', 'w')
    for file in files:
        # save_list.write(file.split('/')[-1]+'\n')
        save_list.write(file+'\n')
    save_list.close()