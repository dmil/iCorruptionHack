"""
Check the FEC website to find if a new filing has been posted.
If there is a new filing store it in /data folder with new date.

http://www.fec.gov/finance/disclosure/ftpdet.shtml

indiv16.zip 
oth16.zip
"""

from app import root
import peewee
import os, subprocess
from datetime import date
import hashlib

from models import File

def sha1OfFile(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()

def download_files(new_folder_path):
    '''
    Get files from FEC and put them in a tmp folder
    '''
    subprocess.call(['sh', root+'/download.sh', new_folder_path])
    download_files
    
def already_downloaded(filepath):
    '''
    Return true if we already have this version of the file
    (check date and file hash). False otherwise
    '''
    try:
        File.get(File.sha1 == sha1OfFile(filepath))
        return True
    except peewee.DoesNotExist:
        return False

def download():
    '''Grabs the latest.'''

    # Download Files
    date_str = date.today().strftime("%Y_%m_%d")
    new_folder_path = "data/downloaded_%s" % date_str
    download_files(new_folder_path)

    # Delete if already exist in database
    for path, subdirs, files in os.walk(new_folder_path):
        for f in files:   
            if already_downloaded(path + '/' + f):
                print "Didn't save '%s' because it was already in the database." % f
                os.remove(path + '/' + f)
            else:
                print "Saved new file '%s/%s'" % (path, f)


download()
