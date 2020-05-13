import pandas as pd
import numpy as np
import os
import sqlite3

class CCF:
    'ccf推荐列表相关'

    root_directory = None       # 根目录
    db_file = None              # 数据库文件
    kinds = ['推荐国际学术期刊','推荐国际学术会议']
    ranks = ['A', 'B', 'C']
    ccf_list = None
    

    def __init__(self, root_directory = os.path.dirname(__file__)): # 默认为当前目录下
        if root_directory:
            self.root_directory = root_directory
        else:
            print('运行目录为代码所在目录')
            self.root_directory = '.'
        self.db_file = self.root_directory + '/../db/build/ccf.db'
        
        print('当前目录；', os.getcwd())
        print('设置的根目录：', self.root_directory)
        print('设置的根目录：', len(self.root_directory))
        print('数据库文件：', self.db_file)
    
    def update_ccf_list(self):
        # 从数据库获取ccf_list
        print('正在从数据库获取ccf_list')
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            print ("连接数据库成功：", self.db_file)
        except Exception as e:
            print("连接数据库失败:", self.db_file ,e)
        try:
            self.ccf_list = cursor.execute('select fullname,shortname from ccf;').fetchall()
            print('select fullname,shortname from ccf：', len(self.ccf_list))
        except Exception as e:
            print( '查询数据失败:',e)
        cursor.close()
        conn.close()  
        print('获取ccf_list成功:', len(self.ccf_list))
        #print(self.get_ccf_list())
        return self.ccf_list
        
    def run(self):
        print('--------------开始读取数据库的ccf数据-----------------')
        self.update_ccf_list()
        print('ccf_list长度：', len(self.ccf_list))
        print('--------------ccf数据读取成功-----------------')
        return self.ccf_list
        
if __name__ == '__main__':
    ccf = CCF()
    ccf.run()
    print('ccf_list：', len(ccf.ccf_list))