import urllib
from skimage.io import imread
import os

mandrill_url = 'http://sipi.usc.edu/database/download.php?vol=misc&img=4.2.03'
fname = 'mandrill.tiff'

def mandrill():
    if os.path.exists(fname):
        pass
    else:
        urllib.urlretrieve(mandrill_url, "mandrill.tiff")
    return imread('mandrill.tiff')



