import pandas as pd 
import numpy as np
import os
import sqlite3

# 使用方法
# root_directory和db可以进行修改，但是要保证root_directory下存在“标题.csv”和“中国计算机学会推荐国际学术会议和期刊目录-2019.csv”，且db指向数据库文件

root_directory = 'E:/GraduationProject/test2/'       # 根目录
read_title_csv = root_directory + '/标题.csv'
read_data_csv =  root_directory + '/中国计算机学会推荐国际学术会议和期刊目录-2019.csv'
write_csv_floder = root_directory + 'csv文件/'
kinds = ['推荐国际学术期刊','推荐国际学术会议']
ranks = ['A', 'B', 'C']
titles = [x[0] for x in pd.read_csv(read_title_csv, header=None).values]

#数据库目录
db = 'E:/GraduationProject/test2/ccf.db'
#db = root_directory + 'ccf.db'

def toCSV():
    print('读取数据文件：',read_data_csv)
    data = pd.read_csv(read_data_csv, header=None)
    print('读取数据文件成功：',read_data_csv)
    if not os.path.exists(write_csv_floder):
        print('目录不存在，生成文件夹：',write_csv_floder)
        os.mkdir(write_csv_floder)
    print('正在写csv文件，存放目录：',write_csv_floder)
    count = 0
    for i in range(len(data)):
        if i == 0:
            temp = [] #生成一个空的list
        elif data.values[i][0].find('序号') != -1:
            # 写csv文件
            df = pd.DataFrame(data=temp, columns=data.values[0][0:5])
            df.to_csv(write_csv_floder + "/{} {} {}.csv".format(titles[count//6], kinds[count%6//3], ranks[count%6%3]), index= False) #index=false表示不加索引列
            print(write_csv_floder + "/{} {} {}.csv".format(titles[count//6], kinds[count%6//3], ranks[count%6%3]))
            # 继续循环
            data_save = []
            count += 1
        else:
            temp.append(data.values[i][0:5])
    print('csv文件写入成功')


def to_ccfTable():
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        print ("连接数据库成功：", db)
    except Exception as e:
        print("连接{}数据库失败:".format(db) ,e)
        return
        
    print('读取数据文件：',read_data_csv)
    data = pd.read_csv(read_data_csv, header=None)
    print('读取数据文件成功：',read_data_csv)
    
    print('正在向ccf表写入数据')
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
    print('ccf数据表的数据导入成功：', db)
    
def to_ProjectTable():
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        print ("连接数据库成功：", db)
    except Exception as e:
        print("连接{}数据库失败:".format(db) ,e)
        return
        
    print('正在向project表写入数据')
    for i in range(len(titles)):
        try:
            cursor.execute('insert into Project (project,name) values (?, ?);', (i, titles[i]))
            print('insert into CCF (project,name) values ({}, {});'.format(i, titles[i]))
        except Exception as e:
                print(i, "%s" % '添加数据失败:',e)
    conn.commit()
    cursor.close()
    conn.close()
    print('project数据表的数据导入成功：', db)

#运行
def main():
    toCSV()
    to_ccfTable()
    to_ProjectTable()

if __name__ == '__main__':
    main()
