import numpy as np
"""
->dataloader
label = h5f['label'][:].swapaxes(0, 2)
label = instance_label(label)  # add here
"""

def instance_label(label):  # label:numpy_array
    conti = 1
    for q in range(1, 5):
        for n in range(1, 9):
            key = 10 * q + n
            label[np.where(label == key)] = conti
            conti += 1
    return label
