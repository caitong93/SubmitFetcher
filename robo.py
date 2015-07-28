# -*- coding: utf-8 -*-
from requests import Session
from MyDB import MyDB
from datetime import datetime

"""
column_fmts = ["columns[%d][data]",
               "columns[%d][name]",
               "columns[%d][searchable]",
               "columns[%d][orderable]",
               "columns[%d][search][value]",
               "columns[%d][search][regex]",
               ]
"""

# decode tuple data from database to friendly string
def tuple_to_str(*args):
    args = args[0]
    return  ' '.join( [ args[2], str(args[0]), args[1], args[3], args[6], str(datetime.fromtimestamp(args[-1])) ] )

class SubmitFetcher:
    def __init__(self):
        _s = Session()
        _s.headers.update({'Accept': 'application/json, text/javascript, */*; q=0.01'})
        _s.headers.update({'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3'})
        _s.headers.update({'Accept-Encoding': 'gzip, deflate'})
        _s.headers.update({'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
        _s.headers.update({'X-Requested-With': 'XMLHttpRequest'})
        _s.headers.update({'Pragma': 'no-cache'})
        
        self._s = _s
    
    # fetch someone`s AC records, decodes into tuples, insert into DB
    # will fetch all until some record is already in DB
    def fetch(self, user):
        print "start fetch AC submits of %s...." % user
        msg = ["draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=false&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=false&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=false&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=false&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=false&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=false&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=false&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%5D%5Bname%5D=&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=false&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B10%5D%5Bdata%5D=10&columns%5B10%5D%5Bname%5D=&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=false&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=11&columns%5B11%5D%5Bname%5D=&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=false&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=0&order%5B0%5D%5Bdir%5D=desc&", "start=%d&length=%d", "&search%5Bvalue%5D=&search%5Bregex%5D=false&un=", "username", "&OJId=All&probNum=&res=1&language=&orderBy=run_id"]
        start = 0
        length = 100
        s = self._s
        db = MyDB()
        _exit = 0
        # (rid, pid, user, oj, mem, rtm, lang, bytes, sub_date)
        while not _exit:
            payload = msg[0] + (msg[1] % ( start, length )) + msg[2] + user + msg[4]
            start += length
            r = s.post('http://acm.hust.edu.cn/vjudge/problem/fetchStatus.action', data=payload)
            data = r.json()['data']
            
            print "%d record fetched" % len(data)
            
            sz = len(data)
            
            if sz:
                trunk = ( VJ_AC_Record(x).get_tuple()  for x in data )
                num = db.try_to_insert(trunk)
                print '%d inserted....' % num
                if num < length:
                    break
            else:
                if start - length == 0:
                    print '%s has no AC record....' % user
                break
            
            if sz < length:
                break

# can turn raw json-converted string into tuple and friendly string                
class VJ_AC_Record:
    # _rid, _user, _oj, _pid, _res, _mem = 0, _time, _lang, _bytes, _sub_time
    def __init__(self, _raw):
        self._data  = _raw
        self._rid   = _raw[0]
        self._user  = _raw[1]
        self._oj    = _raw[11]
        self._pid   = _raw[12]
        self._mem   = _raw[4]
        self._rtm  = _raw[5]
        self._lang  = _raw[6]
        self._bytes = _raw[7]
        self._stamp = _raw[8] / 1000
    
    def get_tuple(self):
        return (self._rid, self._pid, self._user, self._oj, self._mem, self._rtm, self._lang, self._bytes, self._stamp)
        
    def __str__(self):
        return ' '.join( [str(self._rid), self._user, self._oj, self._pid, str(datetime.fromtimestamp(self._stamp))] )

# fetch some guys, and print ac nums
def fetch_them():
    fetcher = SubmitFetcher()
    user_list = [ 'CHristLu', 'slowlight', 'MikeZ', 'Jiian', 'rfrith' ]
    for each in user_list:
        fetcher.fetch(each)
    db = MyDB()
    for each in user_list:
        res = db.select_AC_by_user(each)
        tot = len(res)
        print '%s submits %d AC in total...' % (each, tot)

def write_to_file(res, path):
    with open(path, 'w') as f:
        for each in res:
             print >> f, tuple_to_str(each)
        
if __name__ == '__main__':
    db = MyDB()
    name = 'slowlight'
    res = db.select_AC_by_user(name, date_desc = 1)
    
    if len(res) == 0:
        print 'no records of <%s> found....' % name
    
    by_date = dict()
    
    from datetime import date
    min_date = date(2015, 7, 1)
    for i in res:
        _date = datetime.fromtimestamp( i[-1] ).date()
        if _date < min_date:
            break
        if _date in by_date:
            by_date[_date].append(i)
        else:
            by_date[_date] = [i]
    for k in by_date.keys():
        print k, len(by_date[k])