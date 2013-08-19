import re, os, datetime

R = re.compile(r"(\d+\.\d+(\.\d+)*)")

def break_filename(filename):
    filename = os.path.basename(filename)
    if filename.lower().endswith(".crx"):
        filename = filename[:-4]

    ret = {
        'crxname': filename,
        'version': ''
    }
    t = R.findall(filename)
    if t:
        ret['crxname'] = filename.replace(t[0], '').strip('-')
        ret['version'] = t[0]

    return ret
