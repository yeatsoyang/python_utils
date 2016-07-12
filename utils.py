#-*- coding: utf-8 -*-

import os
import re
import datetime
import random
import math
import xlrd
import csv
from flask import session


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1] in('jpg', 'png')





def mask_mobile(mobi):
    pt = r'^(\d+)\d{4}(\d)$'
    masked = re.sub(pt, r'\1****\2', mobi, re.I|re.S)
    return masked



#产生8位随机字符串
def gen_rnd_str(length=8):
    _s = '1234567890abcdefghijklmnopqrstuvwxyz'
    return ''.join(reduce(lambda x,y: x+[_s[random.randint(0, len(_s)-1)]],
                          range(0, length), []))





def to_utf8(obj, encoding='utf-8'):
    if isinstance(obj, str):
        return obj.decode(encoding)
    return obj







#字典转utf-8编码
def to_utf8_dict(d, encoding='utf-8'):
    assert hasattr(d, 'iteritems')
    return dict([(k, to_utf8(v, encoding=encoding)) \
                     for k, v in d.iteritems()])




def is_nan(a):
    return (isinstance(a, float) and math.isnan(a)) or a!=a





def _float(text):
    if not text:
        return 0.0
    if isinstance(text, float) or isinstance(text, int):
        return text
    if re.match(r'^(?:[-+])?\d+(?:\.\d+)?$', text):
        return float(text)
    return 0.0





def _int(text):
    if not text:
        return 0
    if isinstance(text, int):
        return text
    if re.match(r'^(?:[-+])?\d+$', text):
        return int(text)
    return 0






def _date(text):
    pt_date_1 = r'^(?P<y>\d{4})(?P<mon>\d{2})(?P<d>\d{2})'
    pt_date_2 = r'^(?P<y>\d{4})[./-](?P<mon>\d{1,2})[./-](?P<d>\d{1,2})'
    pt_time = r'(?P<hh>\d+)\:(?P<mm>\d+)\:(?P<ss>\d+)'
    pts = (pt_date_2 + r'\s+' + pt_time,
           pt_date_2,
           pt_date_1,
           )
    for pt in pts:
        m = re.search(pt, text, re.I|re.S)
        if m:
            _m = m.groupdict()
            if 'y' in _m:
                y = int(_m['y'])
                mon = int(_m['mon'])
                d = int(_m['d'])
                if 'hh' in _m:
                    hh = int(_m['hh'])
                    mm = int(_m['mm'])
                    ss = int(_m['ss'])
                    return datetime.datetime(y, mon, d, hh, mm, ss)
                else:
                    return datetime.datetime(y, mon, d, 0, 0, 0)
    pt_yyyymm = r'^(?P<y>\d{4})(?P<mon>\d{2})$'
    m = re.search(pt_yyyymm, text, re.I|re.S)
    if m:
        _m = m.groupdict()
        y, mon = int(_m['y']), int(_m['mon'])
        return datetime.datetime(y, mon, 1, 0, 0, 0)





def _xls_text(v):
    if not v:
        return v
    if isinstance(v, str) or isinstance(v, unicode):
        pt = r'^\d+(?:\.0+)$'
        if re.search(pt, v):
            pt = r'\.0+$'
            return re.sub(pt, '', v)
    if isinstance(v, float):
        return _xls_text('%s' % v)
    elif isinstance(v, int) or isinstance(v, long):
        return '%s' % v
    return v





def open_excel(filepath,all_sheets=True):
    if not os.path.isfile(filepath):
        return
    book = xlrd.open_workbook(filepath)
    sheets = book.sheets()
    if len(sheets) <= 0:
        return
    for sheet in sheets:
        for i in xrange(0,sheet.nrows):
            row = sheet.row(i)
            yield i, [_xls_text(c.value) for c in row]
        if not all_sheets:
            break



def open_csv(file_path, charset='gbk'):
    if not os.path.isfile(file_path):
        return
    with open(file_path, 'rb') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            yield i, [to_utf8(v, encoding=charset) for v in row]





def dict_sort():
    dict=[  
        {'id':'4','name':'b'},  
        {'id':'6','name':'c'},  
        {'id':'3','name':'a'},  
        {'id':'1','name':'g'},  
        {'id':'8','name':'f'}  
    ]  
    #dict.sort(lambda x,y: cmp(x['id'], y['id']))    
    dict = sorted(dict, key=lambda x:x['id'])  
    print dict  



def getLoginInfo():
    user_type=session['user_type']




if __name__ == '__main__':
    print _date('2014/5/22')
    print _date('2014-05-22')
    print _date('20140522')
    print _date('2014522')
    print _date('2014/5/22 22:36:04')
    for i, row in open_excel(r'd:\201312.xlsx'):
        print i, row
        break
    
    dict_sort()
