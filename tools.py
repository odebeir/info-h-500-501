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
                 
    assert(name in data_sources)
    fname = '%s.tif'%name
    if os.path.exists(fname):
        return imread(fname)
    else:
        data = urlopen(data_sources[name]).read()
        open(fname,'wb').write(data)
        return imread(fname)

# javascript to hide/show code in ipython notebook
toggle_on_off = '''<script>
    code_show=true; 
    function code_toggle() {
     if (code_show){
     $('div.input').hide();
     } else {
     $('div.input').show();
     }
     code_show = !code_show
    } 
    $( document ).ready(code_toggle);
    </script>
    <FONT COLOR="FF0000">The raw code for this IPython notebook is by default hidden for easier reading.
    <br>To toggle on/off the raw code, click <a href="javascript:code_toggle()">here</a>.</FONT>'''
