import re, os, datetime
from django.db.models import Max

def break_filename(filename):
    filename = os.path.basename(filename)
    if filename.lower().endswith(".crx"):
        filename = filename[:-4]

    ret = {
        'crxname': filename,
        'version': '1.0'
    }
    pos = filename.rfind('-')
    if pos > -1:
        ret['crxname'] = filename[:pos]
        ret['version'] = filename[pos+1:]

    return ret
