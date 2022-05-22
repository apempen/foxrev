# -*- coding: utf-8 -*-
"""
Created on Mon May 16 22:33:52 2022

@author: apemp

handling db by SQLite
"""

import psycopg2
import time
import os


dbparameter = os.environ["DATABASE_PARAMS"]


def init () :
    """
    テーブルの登録

    Returns
    -------
    None.

    """
    global dbparameter
    # connect to fox.db
    conn = psycopg2.connect(dbparameter)
    cur = conn.cursor()
    cur.execute('CREATE TABLE data (timestamp FLOAT ,species TEXT,latitude FLOAT,longitude FLOAT,userID TEXT)')
    conn.commit()
    cur.close()
    conn.close()


def add (species,latitude,longitude,userID) :
    """
    データ追加
    timestampは浮動小数点値time.time()（UNIX時間、UTC 1970/1/1 00:00:00からの経過秒数）を使用

    Parameters
    ----------
    species : string
        e.g."キツネ","リス".
    latitude : float
    longitude : float
    userID : string

    Returns
    -------
    None.

    """
    global dbparameter
    # connect
    conn = psycopg2.connect(dbparameter)
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO data(timestamp,species,latitude,longitude,userID) VALUES({},\'{}\',{},{},\'{}\')'.format(time.time(),species,latitude,longitude,userID)
    )
    conn.commit()
    cur.close()
    conn.close()

def getLastReportTime(userID):
    global dbparameter
    conn = psycopg2.connect(dbparameter)
    cur = conn.cursor()
    cur.execute(
        'SELECT * FROM data WHERE userID = \'{}\' ORDER BY timestamp DESC LIMIT 1;'.format(userID)
    )
    l = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return l


def getLatestData(limit):
    global dbparameter
    conn = psycopg2.connect(dbparameter)
    cur = conn.cursor()
    cur.execute(
        'SELECT * FROM data ORDER BY timestamp DESC LIMIT {};'.format(limit)
    )
    l = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return l

def get ( species = '*' , timeFrom = 0.0 , timeTo = 1e+20 ) :
    """
    設定した条件にあったデータのリストを返します

    Parameters
    ----------
    species : string, optional
        The default is '*'.
    timeFrom : float, optional
        Condition of timestamp. Only data whose timestamp is greater or equal to timeFrom will be fetched.
        The default is 0.0.
    timeTo : TYPE, optional
        Condition of timestamp. Only data whose timestamp is less or equal to timeTo will be fetched.
        The default is 1e+20 (probably big enough).

    Returns
    -------
    l : list
        like [(1234,"キツネ",43.0,141.0,"id1"),(1357,"シカ",43.0,141.1,"id2")].
        list which contains taples from database.

    """
    global dbparameter
    # connect
    conn = psycopg2.connect(dbparameter)
    cur = conn.cursor()
    if( species == '*' ):
        # get all
        cur.execute(
            'SELECT * FROM data WHERE {} <= timestamp AND timestamp <= {}'
            .format(timeFrom,timeTo)
        )
    else:
        # get specific species
        cur.execute(
            'SELECT * FROM data WHERE species = \'{}\' AND {} <= timestamp AND timestamp <= {}'
            .format(species,timeFrom,timeTo)
        )
    l = cur.fetchall()
    # l is like [(1234,"キツネ",43.0,141.0,"abc"),(1357,"シカ",43.0,141.1,"def")]
    cur.close()
    conn.close()
    return l


def drop () :
    """
    テーブルを消去します

    Returns
    -------
    None.

    """
    global dbparameter
    # connect
    conn = psycopg2.connect(dbparameter)
    cur = conn.cursor()
    cur.execute('DROP TABLE data')
    conn.commit()
    cur.close()
    conn.close()



# if __name__ == "__main__":
#     # drop()
#     init()
#     add("リス",1,2,"id")
#     add("キツネ",2,3,"id2")
#     time.sleep(1)
#     add("リス",5,6,"id3")
#     print(get())
#     print(get(species="リス"))
#     print(get(timeFrom=time.time()-0.5))
