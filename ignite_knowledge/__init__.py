"""
注意这里一定要加，不然会报一个错误
django.core.exceptions.ImproperlyConfigured: Error loading MySQLdb module.
具体原因可能是接口有差异，也可能是版本的问题
"""
import pymysql
pymysql.install_as_MySQLdb()

"""
在Python中，pymysql 是一个用于连接 MySQL 数据库的库。
install_as_MySQLdb() 函数是 pymysql 提供的一个方法，用于将 pymysql 作为 MySQLdb 模块安装。
这样做的目的是为了提供与 MySQLdb 相同的接口，以便可以在需要 MySQLdb 的代码中使用 pymysql。
"""