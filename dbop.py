import pymysql


def iud(q):
    con = pymysql.connect(host='localhost', user='root', password='', port=3306, db='roadsens')
    cmd = con.cursor()
    cmd.execute(q)
    id = con.insert_id()
    con.commit()
    cmd.close()
    con.close()
    return id


def select(q):
    con = pymysql.connect(host='localhost', user='root', password='', port=3306, db='roadsens')
    cmd = con.cursor()
    cmd.execute(q)
    res = cmd.fetchone()
    con.commit()
    cmd.close()
    con.close()
    return res


def selectall(q):
    con = pymysql.connect(host='localhost', user='root', password='', port=3306, db='roadsens')
    cmd = con.cursor()
    cmd.execute(q)
    res = cmd.fetchall()
    con.commit()
    cmd.close()
    con.close()
    return res
