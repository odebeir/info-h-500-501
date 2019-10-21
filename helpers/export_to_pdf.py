import sys
import os

# export all notebook files to pdf files

# list of file to export
source_path = '..'
chapters = sorted([fn for fn in os.listdir(source_path) if '99-' > fn > '00-'])

print(chapters)

file_to_convert = ['../Index.ipynb']

for c in chapters:
    #print(os.listdir(os.path.join(source_path,c)))
    notebooks = sorted([nb for nb in os.listdir(os.path.join(source_path,c)) if '99-' > nb > '00-'])
    print(notebooks)

    for nb in notebooks:
        file_to_convert.append(os.path.join(source_path,c,nb))

print(file_to_convert)

# convert each file to html
for id,fn in enumerate(file_to_convert):
    print('convert[%d]: '%id +fn)
    # > jupyter nbconvert --to html notebook.ipynb
    command = 'jupyter nbconvert --to html "'+ fn + '" --stdout > ../pdf/temp.html'
    os.system(command)

    # convert each file to pdf
    # > wkhtmltopdf notebook.html notebook.pdf
    command = 'wkhtmltopdf ../pdf/temp.html ../pdf/notebook_%02d.pdf'%id
    os.system(command)


# join all pdf files
command = 'pdftk ../pdf/*.pdf cat output ../pdf/merged.pdf'
os.system(command)
