from __future__ import division

from collections import OrderedDict
import numpy as np
from bokeh.plotting import figure, show
from bokeh.models.glyphs import Text
from bokeh.models import HoverTool, ColumnDataSource

def ima_to_rgba32(ima,alpha=1.,mask=None,invert_order=False,string=False):
    """ convert an image to a 32bit per pixel image
    """
    if ima.ndim == 3:
        m,n,p = ima.shape
        img = np.empty((m,n), dtype=np.uint32)
        view = img.view(dtype=np.uint8).reshape((m, n, 4))
        if invert_order:
            for i in range(m):
                for j in range(n):
                    view[i, j, 2] = ima[i,j,0]
                    view[i, j, 1] = ima[i,j,1]
                    view[i, j, 0] = ima[i,j,2]
                    view[i, j, 3] = 255*alpha
        else:
            for i in range(m):
                for j in range(n):
                    view[i, j, 0] = ima[i,j,0]
                    view[i, j, 1] = ima[i,j,1]
                    view[i, j, 2] = ima[i,j,2]
                    view[i, j, 3] = 255*alpha
    
    if ima.ndim == 2:
        m,n = ima.shape
        img = np.empty((m,n), dtype=np.uint32)
        view = img.view(dtype=np.uint8).reshape((m, n, 4))
        if invert_order:
            for i in range(m):
                for j in range(n):
                    view[i, j, 2] = ima[i,j]
                    view[i, j, 1] = ima[i,j]
                    view[i, j, 0] = ima[i,j]
                    view[i, j, 3] = 255*alpha
        else:
            for i in range(m):
                for j in range(n):
                    view[i, j, 0] = ima[i,j]
                    view[i, j, 1] = ima[i,j]
                    view[i, j, 2] = ima[i,j]
                    view[i, j, 3] = 255*alpha

    if mask is not None:
        view[:,:,3] = mask
    
    if string:
        return ['#%x'%(c & 0x00ffffff) for c in img.flatten()]
    else:         
        return img,m,n

def bk_image(ima,title="",flip=False):
    """ Display a simple image in Bokeh mode
    """
    img,m,n = ima_to_rgba32(ima)
   
    fig = figure(x_range=[0,n], y_range=[0,m],title=title)
    if flip:
        fig.image_rgba(image=[img[-1::-1,:]], x=[0], y=[0], dw=[n], dh=[m])
    else:
        fig.image_rgba(image=[img], x=[0], y=[0], dw=[n], dh=[m])
    show(fig);  # open a browser
    
def bk_image_hoover(ima,show_xy=False,show_value=True):
    """ Display a simple image in Bokeh mode + hoover tool (level + pixel coordinates)
    """
    if ima.ndim == 2:
        m,n = ima.shape[:2]
        x_range = [-1,n]
        y_range = [-1,m]
        value = ima.flatten()
        color = ["#%02x%02x%02x"%(v,v,v) for v in value]
    if ima.ndim == 3:
        m,n,p = ima.shape
        x_range = [-1,n]
        y_range = [-1,m]        
        color = ["#%02x%02x%02x"%(r,g,b) for r,g,b in zip(ima[:,:,0].flatten(),ima[:,:,1].flatten(),ima[:,:,2].flatten())]
        value = ["[%03d,%03d,%03d]"%(r,g,b) for r,g,b in zip(ima[:,:,0].flatten(),ima[:,:,1].flatten(),ima[:,:,2].flatten())]
    
    x,y = np.meshgrid(range(n),range(m))        
    source = ColumnDataSource(
        data=dict(
            value=value,
            x=x.flatten(),
            y=y.flatten(),
            color=color,
            name=['pixel %d' for d in range(len(value))],        
        )
    )
    TOOLS = "hover,save,wheel_zoom,pan,reset"

    p = figure(title='',tools=TOOLS,x_range=x_range,y_range=y_range,x_axis_type=None, y_axis_type=None)
    p.plot_width = min(50*n,1000)
    p.plot_height = min(50*m,1000)
    p.toolbar_location = "left"

    p.rect("x", "y", 1., 1., source=source, fill_alpha=1.,color="color",line_color=None)
    hover = p.select(dict(type=HoverTool))
    d = OrderedDict([])
    if show_value:
        d["value"] = "@value"
    if show_xy:
        d["x"] = "@x"
        d["y"] = "@y"
    hover.tooltips= d
    show(p)
