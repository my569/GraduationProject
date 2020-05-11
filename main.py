from ccf.ccf import CCF
from ieee.ieee import IEEE
from acm.acm import ACM

import os
#url = 'https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=computer&highlight=true&returnType=SEARCH&matchPubs=true&pageNumber=130&returnFacets=ALL'

with open('url.txt', 'r') as f:
    url = f.readline()

ccf = CCF('./ccf', './ccf/ccf.db')
ccf.run()
ccf_list = ccf.get_ccf_list()

'''
save_directory = "./ieee"
ieee = IEEE(url, ccf_list)
ieee.run(20)# 至少找出20篇符合要求的文章
# ieee.test_exportCSV(save_directory)
ieee.exportCSV('./ieee/我的检索结果.csv')
'''

with open('url2.txt', 'r') as f:
    url = f.readline()
print(url)
save_directory = "./acm"
acm = ACM(url, ccf_list)
acm.run(20)# 至少找出20篇符合要求的文章
acm.test_exportCSV(save_directory)
acm.exportCSV('./acm/我的检索结果.csv')
