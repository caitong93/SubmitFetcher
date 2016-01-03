# -*- coding: utf-8 -*-

import json
from time import sleep
from copy import deepcopy

import requests

from conf import DATA_PATH, Ids

HEADER = {
    'Host': 'acm.hust.edu.cn',
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0",
    'Accept': "application/json, text/javascript, */*; q=0.01",
    'Accept-Encoding': "gzip, deflate",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'X-Requested-With': "XMLHttpRequest",
    'Referer': "http://acm.hust.edu.cn/vjudge/problem/status.action"
}

COLUMN = {
    'data': '',
    'name': '',
    'searchable': 'true',
    'orderable': 'false',
    'search': {
        'value': '',
        'regex': 'false'
    }
}

JSON = {
    'draw': '1',
    'columns': {},
    'order': {
        '0':    {
            'column': '0',
            'dir': 'desc'
        }
    },
    'start': '0',
    'length': '20',
    'search': {
        'value': '',
        'regex': 'false'
    },
    'un': '',
    'OJId': 'All',
    'probNum': '',
    'res': '0',
    'language': '',
    'orderBy': 'run_id'
}

URL = 'http://acm.hust.edu.cn/vjudge/problem/fetchStatus.action'

class Crawler(object):

    def __init__(self):
        self.s = requests.session()
        self.s.headers.update(HEADER)

    def run(self):
        result = {}
        for _id in Ids:
            print u'[ start ] %s ......' % _id
            retry = 5
            while retry:
                try:
                    result[_id] = self.craw_by_id(_id)
                    print u'[ done ] %s, %d records fetched' % (_id, len(result[_id]))
                    break
                except:
                    print u'[ retry ] %s ......' % _id
                    continue
            sleep(3)

        assert len(result) == len(Ids)
        self.save(result)

    def craw_by_id(self, _id):
        start = 0
        step = 1000
        payload = self.build_payload(un=_id, length=str(step))

        ret = []
        while True:
            payload['start'] = str(start)
            r = self.s.post(URL, data=payload)
            data = r.json()['data']
            if data:
                ret.extend(r.json()['data'])
            if (len(data) < step):
                break
            start += step

        return ret

    def save(self, data):
        with open(DATA_PATH, 'w') as fp:
            fp.write(json.dumps(data, ensure_ascii=False, indent=4))

    def build_payload(self, **kw):
        payload = deepcopy(JSON)

        for col in range(0, 12):
            tmp = deepcopy(COLUMN)
            tmp['data'] = str(col)
            payload['columns'][str(col)] = tmp

        for k, v in kw.items():
            payload[k] = v

        return payload


def test():
    payload = deepcopy(JSON)
    payload['un'] = 'slowlight'

    payload['start'] = '0'

    for col in range(0, 12):
        tmp = deepcopy(COLUMN)
        tmp['data'] = str(col)
        payload['columns'][str(col)] = tmp

    r = requests.post(URL, headers=HEADER, data=payload)
    print r.status_code
    # print json.dumps(r.json(), ensure_ascii=False, indent=4)

if __name__ == '__main__':
    # test()
    c = Crawler()
    c.run()



