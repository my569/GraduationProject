import pandas as pd 
import numpy as np
import os
import sqlite3

class CCF:
    'ccf推荐列表相关'
    
#    root_directory = 'E:/GraduationProject/test2/'       # 根目录
#    db_file = 'E:/GraduationProject/test2/ccf.db'
#    read_title_csv = root_directory + '/标题.csv'
#    read_data_csv =  root_directory + '/中国计算机学会推荐国际学术会议和期刊目录-2019.csv'
#    write_csv_floder = root_directory + '/csv文件导出/'
#    titles = [x[0] for x in pd.read_csv(read_title_csv, header=None).values]


    root_directory = ''       # 根目录
    db_file = ''
    read_title_csv = ''
    read_data_csv =  ''
    write_csv_floder = ''
    kinds = ['推荐国际学术期刊','推荐国际学术会议']
    ranks = ['A', 'B', 'C']
    titles = []
    ccf_list = ''
    

    def __init__(self, root_directory = ".", db_file="./ccf.db"): # 默认为当前目录下
        self.root_directory = root_directory
        self.db_file = db_file
        self.read_title_csv = root_directory + '/标题.csv'
        self.read_data_csv =  root_directory + '/中国计算机学会推荐国际学术会议和期刊目录-2019.csv'
        self.write_csv_floder = root_directory + '/csv文件导出/'
        print(os.getcwd())
        print(self.read_title_csv)
        print(self.read_data_csv)
        print(self.db_file)
        self.titles = [x[0] for x in pd.read_csv(self.read_title_csv, header=None).values]
        print('标题列表：', self.titles)
    
    def toCSV(self):
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


    def to_ccfTable(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            print ("连接数据库成功：", self.db_file)
        except Exception as e:
            print("连接{}数据库失败:".format(self.db_file) ,e)
            return

        print('读取数据文件：',self.read_data_csv)
        data = pd.read_csv(self.read_data_csv, header=None)
        print('读取数据文件成功：',self.read_data_csv)

        print('\n正在向ccf表写入数据')
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
                    print(i, "%s" % '添加数据失败:',e)
        conn.commit()
        cursor.close()
        conn.close()
        print('ccf数据表的数据导入成功：', self.db_file)
    
    def to_ProjectTable(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            print ("连接数据库成功：", self.db_file)
        except Exception as e:
            print("连接{}数据库失败:".format(self.db_file) ,e)
            return

        print('\n正在向project表写入数据')
        for i in range(len(self.titles)):
            try:
                cursor.execute('insert into Project (project,name) values (?, ?);', (i, self.titles[i]))
                print('insert into CCF (project,name) values ({}, {});'.format(i, self.titles[i]))
            except Exception as e:
                    print(i, "%s" % '添加数据失败:',e)
        conn.commit()
        cursor.close()
        conn.close()
        print('project数据表的数据导入成功：', self.db_file)
        
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
        print('获取ccf_list成功')
        #print(self.get_ccf_list())
        return self.ccf_list
    
    def get_ccf_list(self):
        return self.ccf_list
        
    def run(self):
        print('--------------开始处理ccf数据-----------------')
        self.toCSV()
        self.to_ccfTable()
        self.to_ProjectTable()
        self.update_ccf_list()
        print('ccf_list长度：', len(self.ccf_list))
        print('--------------ccf数据处理完成-----------------')
        
if __name__ == '__main__':
    ccf = CCF()
    ccf.run()
    ccf.update_ccf_list()
    print('ccf_list：\n', ccf.get_ccf_list())