import numpy as np
import os
from sklearn.metrics import confusion_matrix
from skimage import draw
from matplotlib import pyplot as plt

class CIFAR10:    
    def __init__(self, path):
        self.path = path
        # Pre-load all data
        self.train = {}
        self.test = {}
        print('Pre-loading training data')
        self.train['images'] = np.load(os.path.join(path, 'images.npy')).astype('uint8')
        self.train['hog'] = np.load(os.path.join(path, 'images_hog.npy'))
        self.train['labels'] = np.load(os.path.join(path, 'labels_.npy')).astype('uint8')
        print('Pre-loading test data')
        self.test['images'] = np.load(os.path.join(path, 'test_images.npy')).astype('uint8')
        self.test['hog'] = np.load(os.path.join(path, 'test_images_hog.npy'))
        self.test['labels'] = np.load(os.path.join(path, 'test_labels.npy')).astype('uint8')
        
        self.labels = ['Airplane', 'Bird', 'Horse']


def evaluate_classifier(clf, test_data, test_labels):
    pred = clf.predict(test_data)
    C = confusion_matrix(pred, test_labels)
    return C.diagonal().sum()*100./C.sum(),C


def get_hog_image(hog, output_size):
    orientations = 16
    cells = 4
    pxcell = output_size//cells
    
    radius = pxcell//2 - 1
    orientations_arr = np.arange(orientations)
    orientation_bin_midpoints = (np.pi * (orientations_arr + .5) / orientations)
    dr_arr = radius * np.sin(orientation_bin_midpoints)
    dc_arr = radius * np.cos(orientation_bin_midpoints)
    if( hog.min() < 0 ): # If we are looking at neural network weights
        hog_image = np.zeros((cells*pxcell, cells*pxcell,3), dtype=float)
        norm = np.abs(hog).max()
    else: # If we are looking at actual HoGs from the dataset
        hog_image = np.zeros((cells*pxcell, cells*pxcell), dtype=float)
    for r in range(cells):
        for c in range(cells):
            for o, dr, dc in zip(orientations_arr, dr_arr, dc_arr):
                centre = tuple([r * pxcell + pxcell // 2,
                                c * pxcell + pxcell // 2])
                rr, cc = draw.line(int(centre[0] - dc),
                                   int(centre[1] + dr),
                                   int(centre[0] + dc),
                                   int(centre[1] - dr))
                if hog.min() < 0:
                    if( hog[r,c,o] >= 0 ):
                        hog_image[rr, cc, 2] += hog[r, c, o]/norm
                    else:
                        hog_image[rr, cc, 0] -= hog[r, c, o]/norm
                else:
                    hog_image[rr, cc] += hog[r, c, o]
    return hog_image