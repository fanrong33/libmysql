# encoding: utf-8

"""
A Friendly pymysql CURD Class

@author 蔡繁荣
@version 0.1 build 20171216
SQL Injection Warning: pymysql.escape_string(value)
"""


# 单例模式获取 mysql connection
def get_mysql(config=None):
    if config is None:
        return 

    connection = MySQL(
        host     = config.get('host'),
        user     = config.get('user'),
        password = config.get('password'),
        db       = config.get('db'),
        port     = config.get('port'),
        charset  = config.get('charset'))
    return connection


import pymysql

class MySQL:
    """A Friendly pymysql Class, Provide CRUD functionality"""

    def __init__(self, host, user, password, db, port=3306, charset='utf8'): 
        # 注意：utf8 important! 而不是 utf-8
        # 否则可能会导致错误 self.encoding = charset_by_name(self.charset).encoding AttributeError: 'NoneType' object has no attribute 'encoding'
        self.host       = host
        self.user       = user
        self.password   = password
        self.db         = db
        self.port       = int(port)
        self.charset    = charset
        self.connection = pymysql.connect(
                host        = self.host,
                user        = self.user,
                password    = self.password,
                db          = self.db,
                port        = self.port,
                charset     = self.charset,
                cursorclass = pymysql.cursors.DictCursor)
        self.last_query = ''



    def insert(self, table, data):
        with self.connection.cursor() as cursor:

            col_list = []
            val_list = []
            for key, val in data.items():
                col_list.append(key)
                # 对数据进行安全性处理
                val = pymysql.escape_string(val) if type(val) == str else "{}".format(val)
                val_list.append("'{}'".format(val))
            
            col_string = ','.join(col_list)
            val_string = ','.join(val_list)

            sql = "INSERT INTO {table} ({fields}) VALUES ({vals})".format(
                table=table, fields=col_string, vals=val_string)

            try:
                self.last_query = sql
                cursor.execute(sql)
                last_id = self.connection.insert_id()

                self.connection.commit()
                return last_id
            except:
                self.connection.rollback()

            return None

    def close(self):
        if getattr(self, 'connection', 0):
            return self.connection.close()

    def __del__(self):
        self.close()

