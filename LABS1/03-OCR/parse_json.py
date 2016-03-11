
import matplotlib.pyplot as plt
from skimage.io import imread
import numpy as np
from skimage.measure import label,regionprops
from matplotlib.patches import Rectangle
import json
import os
from collections import Counter
import pandas as pd

super_file = 'super.json'
supervision = json.load(open(super_file,'rt'))
letters = [v for k,v in supervision.iteritems()]

df = pd.DataFrame(data=letters,columns=['symbol'])

print df.groupby(['symbol']).count()



