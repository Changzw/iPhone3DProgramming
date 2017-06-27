#!/usr/bin/python

####  pyblog module:
# svn checkout http://python-blogger.googlecode.com/svn/trunk/ pyblog
# cd pyblog/pyblog
# python setup.py install

####  colorama module:
# http://pypi.python.org/pypi/colorama

####  pyenchant module:

# http://www.rfk.id.au/software/pyenchant/download.html
# On Mac, 'sudo port install enchant'
# And for the dictionary:
#
#   wget ftp://ftp.gnu.org/gnu/aspell/dict/en/aspell6-en-6.0-0.tar.bz2
#   tar -xvjf aspell6-en-6.0-0.tar.bz2
#   cd aspell6-en-6.0-0
#   ./configure
#   make
#   sudo make install

import shutil
import pyblog
import getpass
import codecs
import os
import glob
import zipfile
import tarfile
from ftplib import FTP
import colorama
from enchant.tokenize import get_tokenizer, HTMLChunker
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter
import enchant

try: import itertools
except ImportError: mymap, myzip= map, zip
else: mymap, myzip= itertools.imap, itertools.izip

colorama.init()

if True:
    try:
        shutil.rmtree('iPhone3D')
    except:
        pass
    
    print "Exporting SVN repo..."
    os.system('svn export . iPhone3D')
    os.remove('iPhone3D/package.py')
    os.remove('iPhone3D/index.html')

print "Unzipping..."

for root, dirs, files in os.walk("iPhone3D"):
    for f in files:
        fullpath = os.path.join(root, f)
        if f.endswith('zip'):
            zip = zipfile.ZipFile(fullpath, 'r')
            zip.extractall("iPhone3D")
            zip.close()
            os.remove(fullpath)

print "Zipping..."

def zipper(dir, zip_file):
    zip = zipfile.ZipFile(zip_file, 'w', compression=zipfile.ZIP_DEFLATED)
    root_len = len(os.path.abspath(dir))
    for root, dirs, files in os.walk(dir):
        archive_root = os.path.abspath(root)[root_len:]
        for f in files:
            fullpath = os.path.join(root, f)
            archive_name = os.path.join(archive_root, f)
#           print "Zipping %s to %s" % (fullpath, archive_name)
            zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
    zip.close()
    return zip_file

try:
    os.remove('iPhone3D.zip')
except:
    pass

zipper("iPhone3D", "iPhone3D.zip")

print colorama.Fore.WHITE + colorama.Back.RED
os.system('svn status -q')
print colorama.Fore.RESET + colorama.Back.RESET
print "DON'T FORGET TO UPDATE SVN "
