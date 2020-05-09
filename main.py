from ccf.ccf import CCF
from ieee.ieee import IEEE


ccf = CCF('./ccf', './ccf/ccf.db')
ccf.run()
ccf_list = ccf.get_ccf_list()


save_directory = "E:/GraduationProject/result"
test = 'https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=computer&highlight=true&returnType=SEARCH&matchPubs=true&pageNumber=130&returnFacets=ALL'

ieee = IEEE(test, ccf_list)
ieee.run()
ieee.test_exportCSV(save_directory)