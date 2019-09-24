# encoding: utf-8

"""
MySQL接口使用示例

@version 1.0.1 build 20180107
"""

from libmysql import MySQL

# 获取数据库连接
mysql = MySQL('127.0.0.1', 'root', '', 'test')

# insert 插入数据
data = {'name':'jim', 'age':25}
insert_id = mysql.insert('t_user', data)


# select 查询数据
user_list = mysql.select('t_user', fields='*', where={'age': 25}, order='id asc', limit='0,5')


# find 查询单数据
user = mysql.find('t_user', fields='id,name', where='id=1')


# update 更新数据
data = {'age':22}
effect = mysql.update('t_user', where='id=1', data=data)
print('update {} records success..'.format(effect))


# delete 删除数据
effect = mysql.delete('t_user', where='id=1')
print('deleted {} records success..'.format(effect))

