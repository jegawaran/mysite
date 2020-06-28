import sys
sys.path.insert(0,"/usr/lib/python3/dist-packages/")
import pymysql
pymysql.version_info = (1, 3, 13, "final", 0)
pymysql.install_as_MySQLdb()
