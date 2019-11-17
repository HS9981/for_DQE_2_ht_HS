import os
from datetime import datetime
import sqlite_for_ht
import fnmatch
import shutil


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
            return print(datetime.now(), 'Created directory', self.path_dir, self.name_dir)


class MonitorDir:
    """Class MonitorDir  monitor 'input' directory for given path for changes
        monitor_dir - method to monitor directory for files, create dataframe with list of the files
     """
    def __init__(self, path_dir):
        self.path_dir = path_dir

    def monitor_dir(self):
        # print(self.path_dir)
        path_to_watch = os.path.join(self.path_dir)
        try:
            list_a = list(sqlite_for_ht.HandleTemp.get_exist_file(self))
        except:
            print(datetime.now(), '-', 'Monitoring started')
            list_a = list()
        for file in os.listdir(path_to_watch):
            # print(path_to_watch, file)
            if os.path.isfile(f'{path_to_watch}{file}'):
                # print(f'{path_to_watch}{file}')
                # print(file, os.path.isfile(f'{path_to_watch}{file}'))
                if file not in list_a:
                    sqlite_for_ht.HandleTemp.insert_into(self, file)
                    print(datetime.now(), '-', 'Found file', file)
            else:
                # print('else', file)
                # print(os.path.isfile(file))
                print(datetime.now(), '-', file, '-', 'This is directiry. Ignore.')
        return file



class FileToHandle:
    """To define file formats, send to analyze only valid files"""
    def __init__(self, filename):
        self.filename = filename

    def getformat(self):
        if fnmatch.fnmatch(self.filename, '*.fb2'):
            print(datetime.now(), '-', self.filename, 'has valid formate')
            sqlite_for_ht.HandleTemp.update_table(self, 'fileformat', 'fb2', self.filename)
        else:
            sqlite_for_ht.HandleTemp.update_table(self, 'fileformat', self.filename.split(".")[-1], self.filename)
            print(datetime.now(), '-', self.filename, 'has invalid formate. To remove')


class MoveFile:
    """to move files with invalid format to different location"""
    def __init__(self, filename):
        self.filename = filename

    def move_file_to(self, path_dir, fld_ii):
        self.path_dir = path_dir
        self.fld_ii = fld_ii
        shutil.move(f'{self.path_dir}/{self.filename}', f'{self.path_dir}{self.fld_ii}/{self.filename}')
        print(datetime.now(), '-', 'File', self.filename, 'was moved to', f'{self.path_dir}{self.fld_ii}')
        sqlite_for_ht.HandleTemp.delete_row(self, self.filename)

