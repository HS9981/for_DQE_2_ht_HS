import sqlite3
from datetime import datetime
import traceback


class CreateDB:
    def create_common_table(self):

        conn = sqlite3.connect('for_python_ht.db')
        c = conn.cursor()
        try:
            c.execute("DROP TABLE common_analyze_for_files")
            conn.commit()
            print(datetime.now(), '-', "Delete common_analyze_for_files before creation")
        except:
            print(datetime.now(), '-', "Tried delete common_analyze_for_files. Not exists.")
            traceback.print_exc()

        c.execute("""CREATE TABLE IF NOT EXISTS common_analyze_for_files (
            filename text,
            book_name text,
            number_of_paragraph integer,
            number_of_words integer,
            number_of_letters integer,
            words_with_capital_letters integer,
            words_in_lowercase integer
            )
            """)
        return print(datetime.now(), '-', 'Created', 'common_analyze_for_files', 'table in sqlite', sep=' ')
        conn.commit()


class CreateTable:

    def insert_into(self, file, title):
        self.file = file
        self.title = title
        conn = sqlite3.connect('for_python_ht.db')
        c = conn.cursor()
        c.execute("INSERT INTO common_analyze_for_files (filename, book_name)  VALUES ('"+self.file+"', '"+self.title+"')")
        conn.commit()
        return None

    def update_table(self, file, column, value):
        self.file = file
        self.column = column
        self.value = value
        conn = sqlite3.connect('for_python_ht.db')
        c = conn.cursor()
        try:
            print(datetime.now(), '-', self.column, int(self.value), self.file)
            c.execute("UPDATE common_analyze_for_files set {} = {} WHERE filename = '{}'".format(self.column, self.value, self.file))
            conn.commit()
        except:
            print(datetime.now(), '-', "Something went wrong while updating common_analyze_for_files table")
            traceback.print_exc()
        return None


class CreateTableSingle:
    def delete_table(self, filename):
        self.filename = filename
        conn = sqlite3.connect('for_python_ht.db')
        c = conn.cursor()
        try:
            c.execute("DROP table '{}'".format(self.filename))
            conn.commit()
        except Exception:
            print(datetime.now(), '-', "Something went wrong")
            traceback.print_exc()
        return None


class HandleTemp:
    def create_temp(self):
        conn = sqlite3.connect('for_python_ht.db')
        c = conn.cursor()
        try:
            c.execute("DROP TABLE before_diff")
            conn.commit()
            print(datetime.now(), '-', "Delete before_diff before creation")
        except:
            print(datetime.now(), '-', "Tried delete before_diff. Not exists.")
            traceback.print_exc()
        c.execute("""CREATE TABLE IF NOT EXISTS before_diff (
            file_name text,
            fileformat text,
            status text
            )
            """)
        return print(datetime.now(), '-', 'Created', 'before_diff', 'table in sqlite', sep=' ')
        conn.commit()

    def get_exist_file(self):
        conn = sqlite3.connect('for_python_ht.db')
        c = conn.cursor()
        c.execute("""SELECT file_name FROM before_diff""")
        result = c.fetchall()
        my_list = []
        for row in result:
            x = row[0]
            my_list.append(x)
            # print(my_list)
        return my_list


    def get_zero_format(self):
        conn = sqlite3.connect('for_python_ht.db')
        c = conn.cursor()
        c.execute("""SELECT file_name FROM before_diff WHERE fileformat IS NULL""")
        result = c.fetchall()
        my_list = []
        for row in result:
            x = row[0]
            my_list.append(x)
        return my_list

    def get_file_to_move(self):
        conn = sqlite3.connect('for_python_ht.db')
        c = conn.cursor()
        c.execute("""SELECT file_name FROM before_diff WHERE fileformat !='fb2'""")
        result = c.fetchall()
        my_list = []
        for row in result:
            x = row[0]
            my_list.append(x)
        return my_list

    def get_file_to_analize(self):
        conn = sqlite3.connect('for_python_ht.db')
        c = conn.cursor()
        c.execute("""SELECT file_name FROM before_diff WHERE fileformat ='fb2' and status is null """)
        result = c.fetchall()
        my_list = []
        for row in result:
            x = row[0]
            my_list.append(x)
        return my_list

    def insert_into(self, file):
        self.file = file
        conn = sqlite3.connect('for_python_ht.db')
        c = conn.cursor()
        c.execute("INSERT INTO before_diff (file_name) VALUES ('{}')".format(self.file))
        conn.commit()
        return None

    def update_table(self, column, value, file):
        self.file = file
        self.column = column
        self.value = value
        conn = sqlite3.connect('for_python_ht.db')
        c = conn.cursor()
        try:
            c.execute("UPDATE before_diff SET {} = '{}' WHERE file_name ='{}'".format(self.column, self.value, self.file))
            print(datetime.now(), '-', "UPDATE before_diff SET {} = '{}' WHERE file_name ='{}'".format(self.column, self.value, self.file))
            # print((self.column, self.value, self.file))
            conn.commit()
        except:
            print(datetime.now(), '-', 'Something went wrong while updating before_diff', self.column, self.value, self.file)
            # print((self.column, self.value, self.file))
            traceback.print_exc()
        return None

    def delete_row(self, file):
        self.file = file
        conn = sqlite3.connect('for_python_ht.db')
        c = conn.cursor()
        try:
            c.execute("DELETE from before_diff WHERE file_name ='{}'".format(self.file))
            # print(self.file)
            conn.commit()
        except:
            print(datetime.now(), '-', 'Something went wrong while deleting ')
            print(datetime.now(), '-', "DELETE from before_diff WHERE file_name ='{}'".format(self.file))
            # print(self.file)
            traceback.print_exc()
        return None
