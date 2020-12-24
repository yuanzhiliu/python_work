import unittest
from todo import Todo
import sys
import io
import pandas as pd
import pymysql


class TestTodo(unittest.TestCase):

    def test_Todo_add_task(self):
        todo = Todo()

        sys.stdin = io.StringIO('测试aaa')
        todo.add_task()

        sql = """select name from to_do_list where now = True"""
        data = todo.show_sql_data(sql)

        self.assertIn('测试aaa', data['name'].values)

        sql = """delete from to_do_list where name = '测试aaa' """
        todo.run_sql(sql)


if __name__ == '__main__':
    unittest.main()
