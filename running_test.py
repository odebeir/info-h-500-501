__author__ = 'olivier'

from runipy.notebook_runner import NotebookRunner
from IPython.nbformat.current import read
import os


def parse(root):
    """returns list of the NB in root
    """
    dirs = sorted([dn for dn in os.listdir(root) if '00'<dn<'99'])
    r = []
    for sub_dir in dirs:
        f = sorted([os.path.join(root,sub_dir,fn) for fn in os.listdir(os.path.join(root,sub_dir)) if ('00'<fn<'99' or fn.startswith('content')) and fn.endswith('.ipynb')])
        r.extend(f)
    return r

nb_filenames = ["Index.ipynb","Index-labs1-6.ipynb"]

nb_filenames.extend(parse('./LABS'))
nb_filenames.extend(parse('.'))

for nb_filename in nb_filenames:
    print('*'*80)
    print(nb_filename)
    print('*'*80)
    notebook = read(open(nb_filename), 'json')
    r = NotebookRunner(notebook)
    r.run_notebook()
