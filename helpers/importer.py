try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
    
from skimage.io import imread
import os

def ext_image(name):
    """
    retrive an image from a url, save a local copy
    """
    data_sources = {'mandrill.tif':
                    'http://sipi.usc.edu/database/download.php?vol=misc&img=4.2.03',
                    'bones.png':
                    'http://homepages.ulb.ac.be/~odebeir/data/bones.png'}
    local_dir = 'data/'             
    assert(name in data_sources)
    fname = os.path.join(local_dir,'%s'%name)
    if os.path.exists(fname):
        return imread(fname)
    else:
        data = urlopen(data_sources[name]).read()
        open(fname,'wb').write(data)
        return imread(fname)


