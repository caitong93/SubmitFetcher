# -*- coding: utf-8 -*-
import sqlite3

class MyDB:
    def __init__(self):
        # create database for each user
        self.db = 'mydb.db3'
        with sqlite3.connect(self.db) as conn:
            c = conn.cursor()
            # init ac table
            c.execute('''create table if not exists fetchedac
                        (rid integer primary key, pid varchar(25), user varchar(50), oj varchar(25), mem integer, rtm integer, lang varchar(25), bytes integer, sub_date integer)''')
            c.close()
            conn.commit()
            #c.execute(''' insert into fetchedac values
            #            (1, '1000', 'slowlight', 'uva', 1000, 1000, 'C++', 1000, 1000)''')    
            
    def test(self):
        pass
            
    def clearDB(self):
        with sqlite3.connect(self.db) as conn:
            c = conn.cursor()
            c.execute('''delete from fetchedac''')
    
    def fetchall(self):
        with sqlite3.connect(self.db) as conn:
            c = conn.cursor()
            c.execute('''select * from fetchedac''')
            res = c.fetchall()
            return res
    
    # select AC records by handle
    def select_AC_by_user(self, name, date_desc = 0):
        sql = ''' select * from fetchedac where user = '%s' ''' % name
        if date_desc:
            sql += 'order by sub_date desc'
        with sqlite3.connect(self.db) as conn:
            c = conn.cursor()
            c.execute(sql)
            res = c.fetchall()
            return res
    
    # try to insert a list of records, return successfully inserted number
    def try_to_insert(self, *args):
        sql = ''' insert into fetchedac values (%d, '%s', '%s', '%s', %d, %d, '%s', %d, %d)'''
        ret = 0
        
        with sqlite3.connect(self.db) as conn:
            c = conn.cursor()
            args = args[0]
            for each in args:
                c.execute(''' select rid from fetchedac where rid = %d ''' % each[0])
                res = c.fetchone()
                if res is None:
                    c.execute(sql%each)
                    ret += 1
                else:
                    return ret
            c.close()
            conn.commit()
            
        return ret

if __name__ == '__main__':
    db = MyDB()
    db.test()