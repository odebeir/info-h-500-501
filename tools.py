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
