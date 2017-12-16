# libmysql
![image](https://img.shields.io/badge/author-fanrong33-blue.svg)
![image](https://img.shields.io/badge/version-0.1-brightgreen.svg)

A Friendly pymysql CURD Class

Based on Mysql.class.php   
   
## 快速开始

### 1、插入数据
```python
import libmysql

config = {'host':'127.0.0.1', 'user':'root', 'password':'', 'db':'test', 'port':3306, 'charset':'utf8'} 
mysql = libmysql.get_mysql(config)

data = {'name':'lilei', 'age':25}
insert_id = mysql.insert('t_user', data)
```

