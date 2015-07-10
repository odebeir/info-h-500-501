from future.standard_library import install_aliases
install_aliases()

from urllib.request import urlopen
from skimage.io import imread
import os

def ext_image(name):
    """
    retrive an image from a url, save a local copy
    """
    data_sources = {'mandrill':
                'http://sipi.usc.edu/database/download.php?vol=misc&img=4.2.03'}
    local_dir = 'data/'             
    assert(name in data_sources)
    fname = os.path.join(local_dir,'%s.tif'%name)
    if os.path.exists(fname):
        return imread(fname)
    else:
        data = urlopen(data_sources[name]).read()
        open(fname,'wb').write(data)
        return imread(fname)

