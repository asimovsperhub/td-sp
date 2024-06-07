import os

import pymysql
from feapder.db.mysqldb import MysqlDB
from feapder.utils.log import log


class Db(object):

    def __init__(self, host: str = "81.71.49.57", database: str = 'crawldata'):
        try:
            self.db = pymysql.connect(
                host=host, port=3306, user="root",
                password="JyMysql@007", database=database, charset="utf8"
            )
        except Exception as e:
            os._exit(0)

    def search(self, sql: str) -> tuple:
        cs = self.db.cursor()
        try:
            cs.execute(sql)
            r = cs.fetchall()
            return r
        except Exception as e:
            return ()
        finally:
            cs.close()

    def insert(self, sql: str):
        cs = self.db.cursor()
        try:
            cs.execute(sql)
            self.db.commit()
            return cs.lastrowid
        except Exception as e:
            print(e)
            self.db.rollback()
        finally:
            cs.close()

    def close_cs_db(self):
        self.db.close()


class MysqlDb(MysqlDB):
    def add(self, sql, exception_callfunc=None):
        """

        Args:
            sql:
            exception_callfunc: 异常回调

        Returns: 添加行数

        """
        affect_count = None
        conn, cursor = None, None

        try:
            conn, cursor = self.get_connection()
            affect_count = cursor.execute(sql)
            conn.commit()

        except Exception as e:
            log.error(
                """
                error:%s
                sql:  %s
            """
                % (e, sql)
            )
            if exception_callfunc:
                exception_callfunc(e)
        finally:
            self.close_connection(conn, cursor)

        return affect_count, cursor.lastrowid


if __name__ == '__main__':
    mysql = MysqlDB()
