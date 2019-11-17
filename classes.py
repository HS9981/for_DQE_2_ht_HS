import os
import sys
from datetime import datetime
import pandas as pd
import re
import time
import sqlite3
import traceback
import sqlite_for_ht
import file_direct

fld_ii = 'incorrect_input'
# path_dir = 'C:/Users/Hanna_Soika/Desktop/arg_test/'
path_dir = str(sys.argv[1])
print(str(sys.argv))
print(path_dir, '-', 'path to monitor')

if not os.path.exists(path_dir):
    os.mkdir(path_dir)
    print(f'{path_dir}')

wrf_tmp_df = pd.DataFrame(columns=['word', 'occurance'])
qwerty = 0


class AnalizeComFile:
    """Analixe given file"""

    def __init__(self, filename):
        self.filename = filename
        self.path = f'{path_dir}'
        # self.path = f'{path_dir}{fld_i}'

    def get_book_name(self):
        """Find book name, inside common_analyze_for_files tag"""
        file_to_read = f'{self.path}/{self.filename}'
        file = open(file_to_read, 'r', encoding='utf-8')
        string_to_match = 'book-title'
        start = '>'
        end = '</'
        for line in file:
            if string_to_match in line:
                matched_line = line
                # print(matched_line)
                matched_line = (matched_line[matched_line.find(start) + len(start):matched_line.rfind(end)])
                # print(matched_line)
                sqlite_for_ht.CreateTable.insert_into(f_1, self.filename, matched_line)
                print(datetime.now(), '-', 'book_name found for', self.filename, '=', matched_line)
                break
        return None

    def get_number_of_paragraph(self):
        """Get number of paragraphs by counting lies starting with <p>"""
        file_to_read = f'{self.path}/{self.filename}'
        file = open(file_to_read, 'r', encoding='utf-8')
        string_to_match = '<p>'
        count = 0
        for line in file:
            if string_to_match in line:
                count += 1
        sqlite_for_ht.CreateTable.update_table(f_1, self.filename, 'number_of_paragraph', count)
        print(datetime.now(), '-', 'number_of_paragraph for', self.filename, 'calculated =', count)
        return None

    def get_number_of_words(self):
        """Exclude tags, exclude binary (img), count words without non literal characters and digits"""
        filename = f'{self.path}/{self.filename}'
        word_counter = {}
        w_cnt = 0
        file = open(filename, 'r', encoding='utf-8')
        data = file.read()
        head, sep, tail = data.partition('<binary')
        head = re.sub('\\s\\s*', ' ', (re.sub('\\W|\\d', ' ', re.sub('<.*?>', '', head))))
        word_list = head.lower().split()
        for word in word_list:
            w_cnt += 1
            if word not in word_counter:
                word_counter[word] = 1
            else:
                word_counter[word] = word_counter[word] + 1
        sqlite_for_ht.CreateTable.update_table(f_1, self.filename, 'number_of_words', w_cnt)
        print(datetime.now(), '-', 'number_of_words for', self.filename, 'calculated =', w_cnt)
        return None

    def get_number_of_letters(self):
        """Exclude tags, exclude binary (img), count words without non literal characters and digits"""
        filename = f'{self.path}/{self.filename}'
        file = open(filename, 'r', encoding='utf-8')
        """Count number of lettes without digits, non letter characters, without xml tags"""
        data = file.read()
        data = re.sub('<.*?binary.*?>*<.*?binary.*?>',' ', data)
        data = re.sub('\\s\\s*', '', (re.sub('\\W|\\d', ' ', re.sub('<.*?>', '', data))))
        let_count = len(data)
        sqlite_for_ht.CreateTable.update_table(f_1, self.filename, 'number_of_letters', let_count)
        print(datetime.now(), '-', 'number_of_letters for', self.filename, 'calculated =', let_count)
        return None

    def get_number_of_words_with_capital_letters_and_lowercase(self):
        """Exclude tags, exclude binary (img), count words without non literal characters and digits"""
        filename = f'{self.path}/{self.filename}'
        file = open(filename, 'r', encoding='utf-8')
        data = file.read()
        head, sep, tail = data.partition('<binary')
        head = re.sub('\\s\\s*', ' ', (re.sub('\\W|\\d', ' ', re.sub('<.*?>', '', head))))
        word_list = head.split()
        upper_cnt = (sum([sum([c.isupper() for c in a]) for a in word_list]))
        lower_cnt = (sum([sum([c.islower() for c in a]) for a in word_list]))
        sqlite_for_ht.CreateTable.update_table(f_1, self.filename, 'words_with_capital_letters', upper_cnt)
        sqlite_for_ht.CreateTable.update_table(f_1, self.filename, 'words_in_lowercase', lower_cnt)
        print(datetime.now(), '-', 'words_with_capital_letters for', self.filename, 'calculated =', upper_cnt)
        print(datetime.now(), '-', 'words_in_lowercase for', self.filename, 'calculated =', lower_cnt)
        return None

    def get_analyze_per_file(self):
        """Complete analyze for file by creating table """
        """Exclude tags, exclude binary (img), count words without non literal characters and digits"""
        filename = f'{self.path}/{self.filename}'
        file = open(filename, 'r', encoding='utf-8')
        df_tmp = pd.DataFrame(columns=['word', 'cnt', 'word_low'])
        w_cnt = 0
        word_counter = {}
        data = file.read()
        head, sep, tail = data.partition('<binary')
        head = re.sub('\s\s*', ' ', (re.sub('\W|\d', ' ', re.sub('<.*?>', '', head))))
        word_list = head.split()
        for word in word_list:
            w_cnt += 1
            if word not in word_counter:
                word_counter[word] = 1
            else:
                word_counter[word] = word_counter[word] + 1

        for word, occurance in word_counter.items():
            df_tmp = df_tmp.append({'word': '{:15}'.format(word), 'cnt': '{:3}'.format(occurance),
                                    'word_low': '{:15}'.format(word).lower()}, ignore_index=True)
        df_tmp = df_tmp.sort_values(by='word_low')
        df_tmp.loc[(df_tmp.word != df_tmp.word_low), 'word'] = 1
        df_tmp.loc[(df_tmp.word == df_tmp.word_low), 'word'] = 0
        df_tmp['word'] = df_tmp.word.astype(int)
        df_tmp['cnt'] = df_tmp.cnt.astype(int)
        df_tmp = df_tmp.groupby(['word_low'])['cnt', 'word'].sum().reset_index()
        conn = sqlite3.connect('for_python_ht.db')
        try:
            try:
                sqlite_for_ht.CreateTableSingle.delete_table(f_3, self.filename)
                print(datetime.now(), '-', self.filename, 'Table deleted at the start point')
            except Exception:
                print(datetime.now(), '-', 'Something went wrong')
                traceback.print_exc()
            df_tmp.to_sql(name=self.filename, con=conn, index=False)
            print(datetime.now(), '-', self.filename, 'Table created and filled with data')
        except Exception:
            print(datetime.now(), '-', 'file with name {} already exists'.format(self.filename))
            traceback.print_exc()
        print(datetime.now(), '-', 'word analyse for', self.filename, 'done')
        sqlite_for_ht.HandleTemp.update_table(f_2, 'status', 'Done', self.filename)
        return None


if __name__ == '__main__':
    g_ii = file_direct.DirectoryChange(path_dir, fld_ii)
    file_direct.DirectoryChange.create_dir(g_ii) # create folder incorect input

    f_tmp = sqlite_for_ht.CreateDB()
    sqlite_for_ht.CreateDB.create_common_table(f_tmp)

    f_1 = sqlite_for_ht.CreateTable()

    f_2 = sqlite_for_ht.HandleTemp()
    sqlite_for_ht.HandleTemp.create_temp(f_2)

    f_3 = sqlite_for_ht.CreateTableSingle()

    while qwerty < 3:
        qwerty +=1
        print(' ')
        print(datetime.now(), '-', 'NEW ITERATION OF ThE WHOLE PROCESS', '№', qwerty, '+ 20 seconds')

        guido_m = file_direct.MonitorDir(path_dir)
        file_direct.MonitorDir.monitor_dir(guido_m)

        sqlite_for_ht.HandleTemp.get_exist_file(f_2)

        ls_nn = list(sqlite_for_ht.HandleTemp.get_zero_format(f_2))
        for i in range(len(ls_nn)):
            xx = file_direct.FileToHandle(ls_nn[i])
            file_direct.FileToHandle.getformat(xx)

        ls_mv = list(sqlite_for_ht.HandleTemp.get_file_to_move(f_2))
        for x in range(len(ls_mv)):
            xx = file_direct.MoveFile(ls_mv[x])
            file_direct.MoveFile.move_file_to(xx, path_dir, fld_ii)

        ls_anlz = list(sqlite_for_ht.HandleTemp.get_file_to_analize(f_2))
        for x in range(len(ls_anlz)):
            xx = AnalizeComFile(ls_anlz[x])
            AnalizeComFile.get_book_name(xx)
            AnalizeComFile.get_number_of_paragraph(xx)
            AnalizeComFile.get_number_of_words(xx)
            AnalizeComFile.get_number_of_letters(xx)
            AnalizeComFile.get_number_of_words_with_capital_letters_and_lowercase(xx)
            AnalizeComFile.get_analyze_per_file(xx)

        sqlite_for_ht.CreateTable.select_result(f_1)

        time.sleep(20)

