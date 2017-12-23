# encoding: utf-8

"""
A Friendly pymysql CURD Class
@author 蔡繁荣
@version 1.0.2 build 20171223
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


    def select(self, table, fields=None, where=None, order=None, limit=None, fetchone=False):
        """
        mysql select() function
        Use sql.PreparedStatement method
        """
        with self.connection.cursor() as cursor:

            prepared = []

            if not fields:
                fields = '*'
            elif isinstance(fields, tuple) or isinstance(fields, list):
                fields = '`{0}`'.format('`, `'.join(fields))
            else:
                fields = fields

            if not where:
                condition = '1'
            elif isinstance(where, dict):
                condition = self._join_field_value(where, ' AND ')
                prepared.extend(where.values())
            elif isinstance(where, int):
                condition = 'id={}'.format(where)
            else:
                condition = where

            if not order:
                orderby = ''
            else:
                orderby = 'ORDER BY {order}'.format(order=order)

            limits = "LIMIT {limit}".format(limit=limit) if limit else ""

            sql = "SELECT {fields} FROM {table} WHERE {where} {orderby} {limits}".format(
                fields=fields, table=table, where=condition, orderby=orderby, limits=limits)

            if not prepared:
                cursor.execute(sql)
            else:
                cursor.execute(sql, tuple(prepared))
            self.connection.commit()
            return cursor.fetchone() if fetchone else cursor.fetchall()


    def find(self, table, fields=None, where=None, order=None, limit=None, fetchone=True):
        return self.select(table, fields, where, order, limit, fetchone)


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


    def bulk_insert(self, table, data):
        assert isinstance(data, list) and data != [], "data format is error"

        with self.connection.cursor() as cursor:

            params = []
            for param in data:
                params.append(pymysql.escape_sequence(param.values(), 'utf-8'))

            values = ', '.join(params)
            fields = ', '.join('`{}`'.format(x) for x in param.keys())

            sql = u"INSERT IGNORE INTO {table} ({fields}) VALUES {values}".format(
                fields=fields, table=table, values=values)

            cursor.execute(sql)
            last_id = self.connection.insert_id()

            self.connection.commit()
            return last_id


    def update(self, table, where=None, data=None):
        """
        mysql update() function
        Use sql.PreparedStatement method
        """
        with self.connection.cursor() as cursor:

            prepared = []
            params = self._join_field_value(data)
            prepared.extend(data.values())

            if not where:
                condition = '1'
            elif isinstance(where, dict):
                condition = self._join_field_value(where, ' AND ')
                prepared.extend(where.values())
            elif isinstance(where, int):
                condition = 'id={}'.format(where)
            else:
                condition = where

            sql = "UPDATE IGNORE {table} SET {params} WHERE {where}".format(
                table=table, params=params, where=condition)

            # check PreparedStatement
            if not prepared:
                result = cursor.execute(sql)
            else:
                result = cursor.execute(sql, tuple(prepared))

            self.connection.commit()
            return result


    def delete(self, table, where=None, limit=None):
        """
        mysql delete() function
        sql.PreparedStatement method
        """
        with self.connection.cursor() as cursor:

            prepared = []

            if not where:
                condition = '1'
            elif isinstance(where, dict):
                condition = self._join_field_value(where, ' AND ')
                prepared.extend(where.values())
            elif isinstance(where, int):
                condition = 'id={}'.format(where)
            else:
                condition = where

            limits = "LIMIT {limit}".format(limit=limit) if limit else ""

            sql = "DELETE FROM {table} WHERE {where} {limits}".format(
                table=table, where=condition, limits=limits)

            if not prepared:
                result = cursor.execute(sql)
            else:
                result = cursor.execute(sql, tuple(prepared))

            self.connection.commit()
            return result


    def count(self, table, where=None):
        """
        count database record
        Use sql.PreparedStatement method
        """
        with self.connection.cursor() as cursor:

            prepared = []

            if not where:
                condition = '1'
            elif isinstance(where, dict):
                condition = self._join_field_value(where, ' AND ')
                prepared.extend(where.values())
            else:
                condition = where

            sql = "SELECT COUNT(*) as cnt FROM {table} WHERE {where}".format(
                table=table, where=condition)

            if not prepared:
                cursor.execute(sql)
            else:
                cursor.execute(sql, tuple(prepared))

            self.connection.commit()
            return cursor.fetchone().get('cnt')


    def query(self, sql, fetchone=False):
        """execute custom sql query"""
        with self.connection.cursor() as cursor:

            cursor.execute(sql)
            self.connection.commit()

            return cursor.fetchone() if fetchone else cursor.fetchall()


    def execute(self, sql):
        """execute custom sql query"""
        with self.connection.cursor() as cursor:

            cursor.execute(sql)
            self.connection.commit()

            return


    def _join_field_value(self, data, glue=', '):
        sql = comma = ''
        for key in data.keys():
            sql += "{}`{}` = %s".format(comma, key)
            comma = glue
        return sql


    def _close(self):
        if getattr(self, 'connection', 0):
            return self.connection.close()


    def __del__(self):
        self._close()

