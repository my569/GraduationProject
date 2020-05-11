import pandas as pd 
import numpy as np
import os
import sqlite3

db_file = '../ccf/ccf.db'
read_data_csv = './acm_list utf8.csv'

def to_ACM_Table():
    print('开始读取acm会议列表数据文件：',read_data_csv)
    data = pd.read_csv(read_data_csv)
    print('读取数据文件成功：',read_data_csv)
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        print ("连接数据库成功：", db_file)
    except Exception as e:
        print("连接{}数据库失败:".format(db_file) ,e)
        
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
    
if __name__ == '__main__':
    to_ACM_Table()