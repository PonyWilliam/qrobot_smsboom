# encoding=utf8
# 读写sqlite数据库
from pathlib import Path
import sqlite3


class Sql(object):
    """处理SQL数据"""

    def __init__(self, db_path: Path) -> None:
        '''初始化数据库'''
        # 数据库路径
        # db_path = Path.cwd().joinpath("api.db")
        # 连接数据库,不检查是否在同一个线程.
        self.client = sqlite3.connect(
            db_path, timeout=6, check_same_thread=False)
        self.cursor = self.client.cursor()
        self.newTable()

    def newTable(self):
        '''初始化表结构'''
        sql = '''
CREATE TABLE IF NOT EXISTS API200 (
   id INT NULL,
   url           TEXT    NOT NULL,
   primary key (url)
);
            '''
        self.cursor.execute(sql)
        self.client.commit()

    def update(self, url):
        '''插入数据'''
        sql = '''
        INSERT INTO API200 (ID,url) VALUES (null,?)
        '''
        try:
            self.cursor.execute(sql, (url,))
            self.client.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def select(self) -> list:
        '''获取所有接口'''
        sql = '''
        SELECT url FROM API200;
        '''
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            urls = []
            for url in result:
                urls.append(url[0])
            return urls
        except Exception as e:
            return

    def __del__(self) -> None:
        '''对象被删除时执行的函数'''
        self.client.close()
