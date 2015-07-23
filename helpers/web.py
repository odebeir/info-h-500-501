from IPython.display import HTML

show_hide = '''<script>code_show=true; 
    function code_toggle() {
     if (code_show){$('div.input').hide();} else {$('div.input').show();}
     code_show = !code_show}
    $( document ).ready(code_toggle);</script>
    <a href="javascript:code_toggle()">show/hide source code</a>
    '''

import os

def files_to_md(path='.',title='Chapter content',indent=0):
    """browses a given directory, returns a markdown formated string
    use i.e. 
    > from IPython.display import Markdown
    > Markdown(files_to_md())
    """
    d = os.listdir(path)
    chapters = sorted([s for s in d if ('00'<=s<='99')])
    if title:
        md = "%s\n%s\n"%(title,'='*len(title))
    else:
        md = ''
    files = sorted([s for s in d if ('00'<=s<='99') and s.endswith('.ipynb')])
    for fn in files:
        link = '%s/%s'%(path,fn)
        md += '%s0. [%s](%s)\n'%(' '*indent,fn[3:-6],link)
    return md

def files_to_html(path='.',title='Chapter content'):
    """browses a given directory, returns a html formated string
    use i.e. 
    > from IPython.display import HTML
    > HTML(files_to_html())
    """
    d = os.listdir(path)
    chapters = sorted([s for s in d if ('00'<=s<='99')])
    if title:
        md = "<h1>\n%s\n</h1>\n"%(title)
    else:
        md = ''
    files = sorted([s for s in d if ('00'<=s<='99') and s.endswith('.ipynb')])
    md += "<ol>\n"
    for fn in files:
        link = '%s/%s'%(path,fn)
        md += '<li><a href="%s">%s</a></li>'%(link,fn[3:-6])
    md += "</ol>\n"
    return md

def chapters_to_md(path='.',title='Outline'):
    """browses a given directory, returns a markdown formated string
    of sbdirectories and files into them
    use i.e. 
    > from IPython.display import Markdown
    > Markdown(chapters_to_md())
    """
    d = os.listdir(path)
    chapters = sorted([s for s in d if ('00'<=s<='99')])
    md = "%s\n%s\n"%(title,'='*len(title))
    for chap in chapters:
        link = '%s/content.ipynb'%chap
        md += '0. [%s](%s)\n'%(chap[3:],link)
        md += files_to_md(path=chap,title=None,indent=4)
    return md

def chapters_to_html(path='.',title='Outline'):
    """browses a given directory, returns a HTML formated string
    of sbdirectories and files into them
    use i.e. 
    > from IPython.display import HTML
    > HTML(chapters_to_html())
    """
    d = os.listdir(path)
    chapters = sorted([s for s in d if ('00'<=s<='99')])
    md = "<h1>\n%s\n</h1>\n"%(title)
    md += "<ol start=0>\n"
    for chap in chapters:
        link = '%s/content.ipynb'%chap
        md += '<li><a href="%s">%s</a></li>'%(link,chap[3:])
        md += files_to_html(path=chap,title=None)
    d += "</ol>\n"
    return md
    
