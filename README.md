# libmysql
![image](https://img.shields.io/badge/author-fanrong33-blue.svg)
![image](https://img.shields.io/badge/version-0.1-brightgreen.svg)

A Friendly pymysql CURD Class

Based on Mysql.class.php   
   
## 快速开始

### 导入Class类
```python
from libmysql import MySQL
```


### 获取数据库连接
使用单例模式
```python
mysql = MySQL('127.0.0.1', 'user', '', 'test')
```


### 插入数据
```python
data = {'name':'lilei', 'age':25}
insert_id = mysql.insert('t_user', data)
```

### 查询数据
```python
user_list = mysql.select('t_user', fields='*', where={'age': 25}, order='id asc', limit='0,5')
```

### 查询单数据
```python
user = mysql.find('t_user', fields='id,name', where='id=1')
```

### 更新数据
```python
data = {'age':22}
effect = mysql.update('t_user', where='id=1', data=data)
print('update {} records success..'.format(effect))
```

### 删除数据
```python
effect = mysql.delete('t_user', where='id=1')
print('deleted {} records success..'.format(effect))
```
