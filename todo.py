import pymysql
import pandas as pd


class Todo:
    SUPPORTED_COMMANDS = ['add', 'show_now', 'show_finish', 'finish', 'clear', 'exit']

    def run(self):
        while True:
            command = input("\n请提供您的命令（add/show_now/show_finish/finish/clear/exit): ")
            if command not in self.SUPPORTED_COMMANDS:
                print('\n')
                print("您输入的指令不支持，请重试.")
                print('\n')
                continue
            if command == 'add':
                self.add()
            elif command == 'show_now':
                self.show_now()
            elif command == 'show_finish':
                self.show_finish()
            elif command == 'finish':
                self.finish()
            elif command == 'clear':
                self.clear()
            else:
                break

    def add(self):
        """增加一条任务"""

        name = input('请输入任务名称：')
        sql = """insert into to_do_list (name, now) values (%s, %s)"""
        values = (name, True)
        self.run_sql(sql, values)

        print('\n' + name + '已添加为当前任务')
        self.show_now()

    def finish(self):
        """选择一项任务标记完成"""

        sql = """
        select name from to_do_list
        where now = True
        """
        data = self.show_sql(sql)

        finish_dir = {}
        key = 1

        if data.empty:
            print('\n当前没有任务')
        else:
            for v in data['name']:
                finish_dir[key] = v
                key = key + 1
            print(finish_dir)
            k = input('请选择已完成的编号：')
            try:
                name = finish_dir[int(k)]
                sql = """update to_do_list set now = False where name = (%s)"""
                values = name
                self.run_sql(sql, values)
                print('\n该任务已完成')
            except KeyError:
                print('无效编号')

            self.show_now()

    def show_now(self):
        """展示所有未完成任务"""

        sql = """
        select name from to_do_list where now = True
        """
        data = self.show_sql(sql)

        if data.empty:
            print('\n当前没有任务')
        else:
            print('\n当前任务有：')
            for v in data['name']:
                print(v)

    def show_finish(self):
        """展示所有完成任务"""

        sql = """
        select name from to_do_list
        where now = False
        """
        data = self.show_sql(sql)

        if data.empty:
            print('\n当前没有未完成任务')
        else:
            print('\n已完成任务有：')
            for v in data['name']:
                print(v)

    def clear(self):
        """清空所有任务"""

        sql = """
        delete from to_do_list
        """
        self.run_sql(sql)

        print('已清空所有数据')

    @staticmethod
    def run_sql(sql, *values):
        """跑sql程序"""
        db = pymysql.connect(host='localhost', user='root', password='700617',
                             database='todo', charset='utf8')
        cursor = db.cursor()
        cursor.execute(sql, *values)
        cursor.close()
        db.commit()
        db.close()

    @staticmethod
    def show_sql(sql):
        """展示SQL数据"""
        db = pymysql.connect(host='localhost', user='root', password='700617',
                             database='todo', charset='utf8')
        return pd.read_sql(sql, db)


def main():
    todo = Todo()
    todo.run()


if __name__ == '__main__':
    main()
