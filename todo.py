import pymysql
import pandas as pd


class Todo:
    SUPPORTED_COMMANDS = ['add', 'show', 'show_finish', 'finish', 'clear', 'exit']

    def run(self):
        while True:
            command = input("\n请提供您的命令（add/show/show_finish/finish/clear/exit): ")
            if command not in self.SUPPORTED_COMMANDS:
                print('\n')
                print("您输入的指令不支持，请重试.")
                print('\n')
                continue
            if command == 'add':
                self.add_task()
            elif command == 'show':
                self.show_task()
            elif command == 'show_finish':
                self.show_task(False)
            elif command == 'finish':
                self.finish_task()
            elif command == 'clear':
                self.clear_all_tasks()
            else:
                break

    def add_task(self):
        name = input('请输入任务名称：')
        sql = """insert into to_do_list (name, now) values (%s, %s)"""
        values = (name, True)
        self.run_sql(sql, values)

        print('\n' + name + '已添加为当前任务')
        self.show_task()

    def finish_task(self):
        sql = """
        select name from to_do_list
        where now = True
        """
        data = self.show_sql_data(sql)['name']
        data.index = data.index + 1
        data.index.name = '编号'

        if data.empty:
            print('\n当前没有任务')
        else:
            print(data)
            k = int(input('请选择已完成的编号：'))
            try:
                values = data[k]
                sql = """update to_do_list set now = False where name = (%s)"""
                self.run_sql(sql, values)
                print('\n该任务已完成')
            except KeyError:
                print('无效的编号')

            self.show_task()

    def show_task(self, now=True):
        if now:
            sql = """select name from to_do_list where now = True"""
        else:
            sql = """select name from to_do_list where now = False"""
        data = self.show_sql_data(sql)

        if data.empty:
            if now:
                print('\n当前没有任务')
            else:
                print('\n当前没有未完成任务')
        if not data.empty:
            if now:
                print('\n当前任务有：')
                for v in data['name']:
                    print(v)
            else:
                print('\n已完成任务有：')
                for v in data['name']:
                    print(v)

    def clear_all_tasks(self):
        sql = """
        delete from to_do_list
        """
        self.run_sql(sql)
        print('已清空所有数据')

    @staticmethod
    def run_sql(sql, *values):
        db = pymysql.connect(host='localhost', user='root', password='700617',
                             database='todo', charset='utf8')
        cursor = db.cursor()
        cursor.execute(sql, *values)
        cursor.close()
        db.commit()
        db.close()

    @staticmethod
    def show_sql_data(sql):
        db = pymysql.connect(host='localhost', user='root', password='700617',
                             database='todo', charset='utf8')
        return pd.read_sql(sql, db)


def main():
    todo = Todo()
    todo.run()


if __name__ == '__main__':
    main()
