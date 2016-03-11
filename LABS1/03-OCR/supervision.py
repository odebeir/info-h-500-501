
import matplotlib.pyplot as plt
from skimage.io import imread
import numpy as np
from skimage.measure import label,regionprops
from matplotlib.patches import Rectangle
import json
import os

plt.ion()


super_file = 'super.json'

try:
    supervision = json.load(open(super_file,'rt'))
except: #no valid json found
    print 'create new supervision'
    supervision = {}

ima = imread('http://homepages.ulb.ac.be/~odebeir/data/doc1.png')
# a letter is darker than the background
th_ima = ima<160
# labeling image
lab, n_label = label(th_ima,return_num=True,background=0)#! bg set to -1
lut = np.arange(1,n_label+1)
np.random.seed(0)
np.random.shuffle(lut) #ensure that the labels are randomly distributed
lut = np.hstack((0,lut)) 
lab = lut[lab+1] #relabel opjects

print len(supervision),n_label

fig = plt.figure(figsize=[20,20])
plt.imshow(th_ima,interpolation='nearest')#,cmap=plt.cm.gray);
ax = plt.gca()

objects = regionprops(lab)

for obj in objects:
    bb = obj['bbox']
    centroid = obj['centroid']
    x0 = bb[1]
    y0 = bb[0]
    w = bb[3]-bb[1]+1
    h = bb[2]-bb[0]+1
    ax.add_patch(Rectangle((x0-1,y0-1),w,h,fc='none',ec='r'))

    extra = 50
    ax.set_xlim([x0-extra,x0+w+extra])
    ax.set_ylim([y0+h+extra,y0-extra])

    l = '%d'%obj['label']
    if supervision.has_key(l):
        plt.text(x0,y0,supervision[l],color='y')
        continue
    plt.draw()
    plt.pause(0.1)

    c = raw_input('letter=')

    if not c:
        break
    else:
        print l
        supervision[l] = c
        plt.text(x0,y0,supervision[l],color='w')
        plt.draw()


json.dump(supervision,open(super_file,'wt'),sort_keys=True,
                            indent=4, separators=(',', ': '))
plt.ioff()
plt.show()
print supervision