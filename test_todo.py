import unittest
from todo import Todo
import sys
import io
import pandas as pd
import pymysql


class TestTodo(unittest.TestCase):

    def test_Todo_add(self):
        todo = Todo()

        sys.stdin = io.StringIO('测试aaa')
        todo.add_task()

        db = pymysql.connect(host='localhost', user='root', password='700617',
                             database='todo', charset='utf8')
        sql = """select name from to_do_list where now = True"""
        data = pd.read_sql(sql, db)

        self.assertIn('测试aaa', data['name'].values)


if __name__ == '__main__':
    unittest.main()
