__author__ = 'olivier'

from runipy.notebook_runner import NotebookRunner
from IPython.nbformat.current import read
#from nbformat import read
import os
import sys
import traceback


def parse(root):
    """returns list of the NB in root
    """
    dirs = sorted([dn for dn in os.listdir(root) if '00'<dn<'99' and os.path.isdir(os.path.join(root,dn))])
    print(dirs)
    r = []
    for sub_dir in dirs:
        f = sorted([os.path.join(root,sub_dir,fn) for fn in os.listdir(os.path.join(root,sub_dir)) if ('00'<fn<'99' or fn.startswith('content')) and fn.endswith('.ipynb')])
        r.extend(f)
    return r

nb_filenames = ["Index.ipynb","Index-labs1-6.ipynb"]

nb_filenames.extend(parse('./LABS'))
nb_filenames.extend(parse('.'))

is_error = False
error_list = []
for nb_filename in nb_filenames:
    try:
        print('*'*80)
        print(nb_filename)
        print('*'*80)
        notebook = read(open(nb_filename), 'json')
        r = NotebookRunner(notebook)
        r.run_notebook()
        r.shutdown_kernel()
        
    except Exception as e:
        is_error = True
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()

        error_list.append((nb_filename,e,ex_type, ex_value, ex_traceback))


# display the summary of all the exceptions
for fn,e, ex_type, ex_value, ex_traceback in error_list:
    print('Failed to EXECUTE: ' + nb_filename + '\n' + str(e))

    # Extract unformatter stack traces as tuples
    trace_back = traceback.extract_tb(ex_traceback)

    # Format stacktrace
    stack_trace = list()

    for trace in trace_back:
        stack_trace.append(
            "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

    print('_' * 80)
    print("Filename : %s " % fn)
    print("Exception type : %s " % ex_type.__name__)
    print("Exception message : %s" % ex_value)
    print("Stack trace :\n%s" % '\n'.join(stack_trace))
    print('-' * 80)

if is_error: # raise one exception if any problem occured
    raise Exception

