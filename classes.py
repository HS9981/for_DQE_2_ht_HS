import os
from datetime import datetime
import pandas as pd
import fnmatch
import shutil
import time
# import traceback
import logging

path_dir = 'C:/Users/Hanna_Soika/Desktop/Python Module'
if not os.path.exists(path_dir):
    os.mkdir(path_dir)
    print(f'{path_dir}')

fld_i = 'input'
fld_ii = 'incorect_input'
global before_df
before_df = pd.DataFrame(columns=['filename', 'fileformat', 'status'])
print ('before_df was created')

analyz_df = pd.DataFrame(columns=['book_name', 'number_of_paragraph', 'number_of_words', 'number_of_letters',
                                  'words_with_capital_letters', 'words_in_lowercase'])
print ('analyz_df was created')

class DirectoryChange:
    """Class DirectoryChange create and monitor 'input' directory for given path for changes
        create_dir - method to create directory
     """
    def __init__(self, path_dir, name_dir):
        self.path_dir = path_dir
        self.name_dir = name_dir

    def create_dir(self):
        folder = os.path.join(self.path_dir, self.name_dir)
        if not os.path.exists(folder):
            os.mkdir(folder)
            print(f'{folder}')
            msg = ' Created directory '
            print(datetime.now(), msg, self.path_dir, "/", self.name_dir, sep='')


class MonitorDir:
    """Class MonitorDir  monitor 'input' directory for given path for changes
        monitor_dir - method to monitor directory for files, create dataframe with list of the files

     """
    def __init__(self, path_dir, name_dir):
        self.path_dir = path_dir
        self.name_dir = name_dir

    def monitor_dir(self):
        global before_df
        path_to_watch = os.path.join(self.path_dir, self.name_dir)

        list_A = list(before_df['filename'].unique())
        for file in os.listdir(path_to_watch):
            if file not in list_A:
                before_df = before_df.append({'filename': file}, ignore_index=True)
                msg = 'Found file'
                print(datetime.now(), msg, file)
            # else:
            #     print(file, 'againg')


class FileToHandle:
    """To define file formats, send to analyze only valid files"""
    def __init__(self, filename):
        self.filename = filename

    def getformat(self):
        global before_df
        if fnmatch.fnmatch(self.filename, '*.fb2'):
            print(datetime.now(), self.filename, 'has valid formate')
            before_df.loc[(before_df.filename == self.filename), 'fileformat'] = 'fb2'
        else:
            before_df.loc[(before_df.filename == self.filename), 'fileformat'] = self.filename.split(".")[-1]
            print(datetime.now(), self.filename, 'has invalid formate. To remove')


class MoveFile:
    """to move files with invalid format to different location"""
    def __init__(self, filename):
        self.filename = filename

    def move_file_to(self):
        global before_df
        before_df = before_df[before_df.filename != self.filename]
        shutil.move(f'{path_dir}/{fld_i}/{self.filename}', f'{path_dir}/{fld_ii}/{self.filename}')
        print(datetime.now(), 'File', self.filename, 'was moved to', f'{path_dir}/{fld_ii}')


class AnalizeComFile:
    """Analixe given file, common table for all files"""
    def __init__(self, filename):
        self.filename = filename

    def create_table(self):
        print('TODO: create table in sqlite to store data if not exist')

    def read_file(self):
        global analyz_df
        print('TODO: implement reading and analyzing file', self.filename)


if __name__ == '__main__':
    while 1:
        time.sleep(5)
        g_ii = DirectoryChange(path_dir, fld_ii)
        DirectoryChange.create_dir(g_ii)

        guido = DirectoryChange(path_dir, fld_i)
        DirectoryChange.create_dir(guido)

        guido_m = MonitorDir(path_dir, fld_i)
        MonitorDir.monitor_dir(guido_m)

        df_ls = before_df[before_df['fileformat'].isnull()]
        ls_nn = list(df_ls['filename'].unique())
        for i in range(len(ls_nn)):
            xx = FileToHandle(ls_nn[i])
            FileToHandle.getformat(xx)

        df_mv = before_df[before_df['fileformat'] != 'fb2']
        ls_mv = list(df_mv['filename'].unique())
        for x in range(len(ls_mv)):
            xx = MoveFile(ls_mv[x])
            MoveFile.move_file_to(xx)

        df_anlz = before_df[(before_df['fileformat'] == 'fb2') & (before_df['status'] != 'Done')]
        ls_anlz = list(df_anlz['filename'].unique())
        for x in range(len(ls_anlz)):
            xx = AnalizeComFile(ls_anlz[x])
            AnalizeComFile.read_file(xx)

        print(before_df)