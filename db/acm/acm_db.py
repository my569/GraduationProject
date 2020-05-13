import pandas as pd 
import numpy as np
import os
import sqlite3

db_file = '../ccf/ccf.db'
read_data_csv = './acm_list utf8.csv'


class ACM_DB:
    'ccf推荐列表相关'

    root_directory = None       # 根目录
    db_file = None              # 数据库文件
    read_data_csv =  None       # acm导出会议列表

    def __init__(self, root_directory = os.path.dirname(__file__)): # 默认为当前目录下
        if root_directory:
            self.root_directory = root_directory
        else:
            print('运行目录为代码所在目录')
            self.root_directory = '.'

        self.db_file = self.root_directory + "/../build/ccf.db"
        self.read_data_csv = self.root_directory + '/acm_list utf8.csv'
        
        print('当前目录；', os.getcwd())
        print('acm导出会议列表文件：', self.read_data_csv)
        print('数据库文件：', self.db_file)

    def to_ACM_Table(self):
        print('开始读取acm会议列表数据文件：', self.read_data_csv)
        data = pd.read_csv(self.read_data_csv)
        print('读取数据文件成功：', self.read_data_csv)
        
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            print ("连接数据库成功：", self.db_file)
        except Exception as e:
            print("连接{}数据库失败:".format(self.db_file) ,e)
            
        for i in range(len(data.values)):
            # 将该行数据存入数据库
            row = data.values[i]
            try:
                cursor.execute('insert into ACM (publication_title,print_identifier,title_url,title_id,publisher_name,parent_publication_title_id) values (?, ?, ?, ?, ?, ?);',
                                            tuple(row))
                print(i, 'insert into ACM (publication_title,print_identifier,title_url,title_id,publisher_name,parent_publication_title_id) values {};'.format(tuple(row)))
            except Exception as e:
                print(i, "%s" % '添加数据失败:',e)
                
        conn.commit()
        cursor.close()
        conn.close()
        return data
       
    def run(self):
        print('--------------开始处理acm数据-----------------')
        data = self.to_ACM_Table()
        print('数据长度：', len(data))
        print('--------------acm数据处理完成-----------------')
    
if __name__ == '__main__':
    acm_db = ACM_DB()
    acm_db.run()