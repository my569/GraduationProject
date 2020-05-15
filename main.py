from ccf.ccf import CCF
from ieee.ieee import IEEE
from acm.acm import ACM

import os
#url = 'https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=computer&highlight=true&returnType=SEARCH&matchPubs=true&pageNumber=130&returnFacets=ALL'

# 获取ccf目录
ccf = CCF()
ccf_list = ccf.run()

op = 0
op = int(input('0:ieee，1:acm\n'))
if op == 0:
    # 读取文件中的url
    with open('url.txt', 'r') as f:
        url = f.readline()
    ieee = IEEE(url, ccf_list)
    ieee.run(20)# 至少找出20篇符合要求的文章
    ieee.exportCSV_byFilefolder("./ieee/result")
    #ieee.exportCSV_byFilename('./ieee/result/我的检索结果.csv')
elif op == 1:
    with open('url2.txt', 'r') as f:
        url = f.readline()
    print(url)
    acm = ACM(url, ccf_list)
    acm.run(20)# 至少找出20篇符合要求的文章
    acm.exportCSV_byFilefolder('./acm/result')
    #acm.exportCSV_byFilename('./acm/result/检索结果.csv')
