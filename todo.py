import pymysql
import pandas as pd


class Todo():
    SUPPORTED_COMMANDS = ['add', 'show_now', 'show_finish', 'finish', 'clear', 'exit']
    db = pymysql.connect(host='localhost', user='root', password='700617',
                         database='todo', charset='utf8')

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

        db = pymysql.connect(host='localhost', user='root', password='700617',
                             database='todo', charset='utf8')
        cursor = db.cursor()
        query = """insert into to_do_list (name, finish) values (%s, %s)"""
        values = (name, '否')
        cursor.execute(query, values)
        cursor.close()
        db.commit()
        db.close()


        print('\n' + name + '已添加为当前任务')
        self.show_now()

    def finish(self):
        """选择一项任务标记完成"""

        db = pymysql.connect(host='localhost', user='root', password='700617',
                             database='todo', charset='utf8')

        sql = """
        select name from to_do_list
        where finish = '否'
        """
        data = pd.read_sql(sql, db)

        dir = {}
        key = 1

        if data.empty:
            print('\n当前没有任务')
        else:
            for v in data['name']:
                dir[key] = v
                key = key + 1
            print(dir)
            k = input('请选择已完成的编号：')
            try:
                name = dir[int(k)]
                cursor = db.cursor()
                query = """update to_do_list set finish = "是" where name = (%s)"""
                values = (name)
                cursor.execute(query, values)
                cursor.close()
                db.commit()
                db.close()
                print('\n该任务已完成')
            except:
                print('无效编号')

            self.show_now()



    def show_now(self):
        """展示所有未完成任务"""

        db = pymysql.connect(host='localhost', user='root', password='700617',
                             database='todo', charset='utf8')

        sql = """
        select name from to_do_list
        where finish = '否'
        """
        data = pd.read_sql(sql, db)

        if data.empty:
            print('\n当前没有任务')
        else:
            print('\n当前任务有：')
            for v in data['name']:
                print(v)

    def show_finish(self):
        """展示所有完成任务"""

        db = pymysql.connect(host='localhost', user='root', password='700617',
                             database='todo', charset='utf8')

        sql = """
        select name from to_do_list
        where finish = '是'
        """
        data = pd.read_sql(sql, db)

        if data.empty:
            print('\n当前没有未完成任务')
        else:
            print('\n已完成任务有：')
            for v in data['name']:
                print(v)

    def clear(self):
        """清空所有任务"""

        db = pymysql.connect(host='localhost', user='root', password='700617',
                             database='todo', charset='utf8')

        sql = """
        delete from to_do_list
        """
        cursor = db.cursor()
        cursor.execute(sql)
        cursor.close()
        db.commit()
        db.close()


        print('已清空所有数据')


def main():
    todo = Todo()
    todo.run()


if __name__ == '__main__':
    main()
