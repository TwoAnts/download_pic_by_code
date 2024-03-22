#!/usr/bin/env python3

import requests
import pyrfc6266
import os
import sys
import re
from pathlib import Path
import time

FN_PATTERN = re.compile(r'filename="(?P<filename>[a-zA-Z0-9_.]+)"')

def adaptive(t, is_done):
    if is_done:
        t -= 0.5
        if t < 1:
            t = 1
    else:
        t += 2
        if t > 8:
            t = 8
    return t

def find_path(dst_dir, code, count):
    fpath = "%s_p%s.*" %(code, count-1)
    for f in dst_dir.glob(fpath):
        return f
    return None

def save_file(dst_dir, resp):
    cd = resp.headers['content-disposition']
    m = FN_PATTERN.search(cd)
    if not m:
        raise Exception("find file name failed: %s" %cd)
    fname = m.group('filename')
    dst = dst_dir / fname
    with dst.open("wb") as of:
        for chunk in resp.iter_content(chunk_size=8192):
            of.write(chunk)
    return fname

def download(code, lineno, dst_dir, errf):
    count = 0
    g_sleep = 1
    count_err = 0
    is_first = True
    while count_err < 5:
        count += 1
        exist_file = find_path(dst_dir, code, count)
        if exist_file:
            print("[%d:%d] ignore %s" %(lineno, count, exist_file))
            continue
        c = code
        if count > 1:
            c = '%s-%s' %(code, count)
        if not is_first:
            time.sleep(g_sleep)
        else:
            is_first = False
        try:
            resp = requests.get('https://pixiv.nl/%s.jpg' %c)
        except Exception as e:
            print("[%d:%d] download %s failed: %s" %(lineno, count, c, e))
            count_err += 1
            g_sleep = adaptive(g_sleep, False)
            continue
        if resp.status_code == 404:
            break
        if not resp.ok:
            g_sleep = adaptive(g_sleep, False)
            count_err += 1
            print("[%d:%d] download %s failed: %s %s" %(lineno, count, c, resp.status_code, resp.reason))
            continue
        fname = save_file(dst_dir, resp)
        g_sleep = adaptive(g_sleep, True)
        print("[%d:%d] download %s" %(lineno, count, fname))
        
    if count_err > 0:
        errf.write("%s\n" %code)

if __name__ == '__main__':
    lineno = 0
    dst_dir = Path(sys.argv[2])
    dst_dir.mkdir(parents=True, exist_ok=True)
    with open(sys.argv[1], 'r', encoding='UTF-8') as f, open(sys.argv[3], 'w', encoding='UTF-8') as errf:
        for line in f:
            lineno += 1
            line = line.strip()
            if not line:
                continue
            download(line, lineno, dst_dir, errf)