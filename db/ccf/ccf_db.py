import pandas as pd
import numpy as np
import os
import sqlite3

class CCF_DB:
    'ccf推荐列表相关'

    root_directory = None       # 根目录
    db_file = None              # 数据库文件
    read_title_csv = None       # 标题
    read_data_csv =  None       # ccf推荐目录
    kinds = ['推荐国际学术期刊','推荐国际学术会议']
    ranks = ['A', 'B', 'C']
    titles = []
    ccf_list = None

    def __init__(self, root_directory = os.path.dirname(__file__)): # 默认为当前目录下
        if root_directory:
            self.root_directory = root_directory
        else:
            print('运行目录为代码所在目录')
            self.root_directory = '.'

        self.db_file = self.root_directory + "/../build/ccf.db"
        self.read_title_csv = self.root_directory + '/标题.csv'
        self.read_data_csv =  self.root_directory + '/中国计算机学会推荐国际学术会议和期刊目录-2019.csv'
        print('当前目录；', os.getcwd())
        print('设置的根目录：', self.root_directory)
        print('标题文件：', self.read_title_csv)
        print('目录文件：', self.read_data_csv)
        print('数据库文件：', self.db_file)
        print('正在读取标题...')
        self.titles = [x[0] for x in pd.read_csv(self.read_title_csv, header=None).values]
        print('读取标题成功，标题列表：', self.titles)
    
    # 数据存不存到csv文件里都行，主要是存数据库
    def toCSV(self):
        self.write_csv_floder = self.root_directory + '/csv文件导出/'
        print('开始读取ccf推荐目录数据文件：',self.read_data_csv)
        data = pd.read_csv(self.read_data_csv, header=None)
        print('读取数据文件成功：',self.read_data_csv)
        if not os.path.exists(self.write_csv_floder):
            print('目标文件夹不存在，正在生成新的文件夹：',self.write_csv_floder)
            os.mkdir(self.write_csv_floder)
        print('正在写csv文件，存放目录：',self.write_csv_floder)
        count = 0
        for i in range(len(data)):
            if i == 0:
                temp = [] #生成一个空的list
            elif data.values[i][0].find('序号') != -1:
                # 写csv文件
                df = pd.DataFrame(data=temp, columns=data.values[0][0:5])
                df.to_csv(self.write_csv_floder + "/{} {} {}.csv".format(self.titles[count//6], self.kinds[count%6//3], self.ranks[count%6%3]), index= False) #index=false表示不加索引列
                print(self.write_csv_floder + "/{} {} {}.csv".format(self.titles[count//6], self.kinds[count%6//3], self.ranks[count%6%3]))
                # 继续循环
                data_save = []
                count += 1
            else:
                temp.append(data.values[i][0:5])
        print('csv文件写入成功')


    def to_CCF_table(self):
        '向CCF表中写数据'
        print('读取数据文件：',self.read_data_csv)
        data = pd.read_csv(self.read_data_csv, header=None)
        print('读取数据文件成功：',self.read_data_csv)
        
        print('\n正在向ccf表写入数据')
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            print ("连接数据库成功：", self.db_file)
        except Exception as e:
            print("连接{}数据库失败:".format(self.db_file) ,e)
            return
        # 这里的代码有点乱，因为整理的csv文件内容比较不规则
        count = 0
        for i in range(len(data)):
            if data.values[i][0].find('序号') != -1: #识别到下一个表格的表头，说明当前表格读到结尾了
                count += 1
            else:
                row = data.values[i]
                # 将该行数据存入数据库
                try:
                    cursor.execute('insert into CCF (fullname,shortname,rank, publisher, website, kind, project) values (?, ?, ?, ?, ?, ?, ?);',
                                                (row[2],   row[1],  count%6%3,row[3],    row[4],count%6//3,count//6))
                    print(i, 'insert into CCF (fullname,shortname,rank, publisher, website, kind, project) values ({}, {}, {}, {}, {}, {}, {});'.format(
                                                row[2],   row[1],  count%6%3,row[3],    row[4],count%6//3,count//6))
                except Exception as e:
                    print(i, "%s" % '添加数据失败:', e)
        conn.commit()
        cursor.close()
        conn.close()
        print('ccf数据表的数据导入成功：', self.db_file)
    
    def to_Project_table(self):
        '向Project(标题、学科)表中写数据'
        
        print('\n正在向project表写入数据')
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            print ("连接数据库成功：", self.db_file)
        except Exception as e:
            print("连接{}数据库失败:".format(self.db_file) ,e)
            return
            
        for i in range(len(self.titles)):
            try:
                cursor.execute('insert into Project (project,name) values (?, ?);', (i, self.titles[i]))
                print('insert into CCF (project,name) values ({}, {});'.format(i, self.titles[i]))
            except Exception as e:
                    print(i, "%s" % '添加数据失败:', e)
        conn.commit()
        cursor.close()
        conn.close()
        print('project数据表的数据导入成功：', self.db_file)
        
    def update_ccf_list(self):
        '从数据库获取ccf_list'
        print('正在从数据库更新ccf_list')
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
        print('更新ccf_list成功:', len(self.ccf_list))
        return self.ccf_list
        
    def run(self):
        print('--------------开始处理ccf数据-----------------')
        # self.toCSV() #想导出的话，可以取消注释
        self.to_CCF_table()
        self.to_Project_table()
        self.update_ccf_list()
        print('ccf_list长度：', len(self.ccf_list))
        print('--------------ccf数据处理完成-----------------')
        return self.ccf_list
        
        
if __name__ == '__main__':
    ccf_db = CCF_DB()
    ccf_db.run()
    ccf_db.update_ccf_list()
    print('ccf_list：', len(ccf_db.ccf_list))