

def pTime(start):
    seconds = timeit.default_timer() - start
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print ('Time:' , "%02d:%02d:%02d" % (h, m, s))


import time
import timeit
import os
import re
import pandas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class IEEE:
    'ieee搜索引擎相关'
    url = 'https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText='
    ccf_list = []
    result = None
    driver = None
    
    def __init__(self, url, ccf_list):
        self.url = url
        self.ccf_list = ccf_list
        print('搜索网址为：', self.url)
    
    def brower_init(self, isheadless = False):
        print("正在初始化浏览器")
        try :
            chrome_options = webdriver.ChromeOptions()
        except exception as e:
            print('请检查是否安装chrome的webdriver', e)
        if isheadless:
            chrome_options.add_argument('--headless')  # 增加无界面选项
        chrome_options.add_argument('--disable-gpu')  # 如果不加这个选项，有时定位会出现问题
        return chrome_options

    def getInfo(self):
        showInfo_script = "function showInfo(node){                                                                                                    \
        var paper_info = {};                                                                                                                           \
        try {                                                                                                                                          \
            home = 'https://ieeexplore.ieee.org';                                                                                                              \
            paper_info['document_title'] = node.getElementsByTagName('h2')[0].innerText;                                                               \
            paper_info['url'] = home + node.getElementsByTagName('h2')[0].getElementsByTagName('a')[0].getAttribute('href');                           \
            paper_info['authors'] = node.getElementsByClassName('author')[0].innerText;                                                                \
            paper_info['publication_title'] = node.getElementsByClassName('description')[0].getElementsByTagName('a')[0].innerText;                    \
            paper_info['description'] = node.getElementsByClassName('description')[0].getElementsByClassName('publisher-info-container')[0].innerText; \
            paper_info['abstract'] = node.getElementsByClassName('js-displayer-content')[0].getElementsByTagName('span')[0].innerText;                 \
        }catch(err) {                                                                                                                                  \
            console.log('%c该节点获取信息有误（可能有部分信息缺失）','color:blue;font-size:15px');                                                     \
            console.log(node);                                                                                                                         \
        }                                                                                                                                              \
        console.log('文章标题:'		 + paper_info['document_title']);                                                                                  \
        console.log('作者:' 		 + paper_info['authors']);                                                                                         \
        console.log('出版物标题：'	 + paper_info['publication_title']);                                                                            \
        console.log('文章说明：'          + paper_info['description']);                                                                                \
        console.log('url：'          + paper_info['url']);                                                                                             \
        console.log('摘要：'       + paper_info['abstract']);                                                                                        \
        return paper_info;                                                                                                                             \
        }\
        function getInfoList(){                                                                                                                            \
            infoList = [];                                                                                                                                  \
            list = document.getElementsByClassName('List-results-items');                                                                                  \
            for (var i = 0; i < list.length; i++) {                                                                                                        \
                console.log(i);                                                                                                                            \
                console.log(list[i]);                                                                                                                      \
                infoList.push(showInfo(list[i]));                                                                                                          \
            }                                                                                                                                              \
            return infoList;                                                                                                                               \
        }\
        return getInfoList();"
        return self.driver.execute_script(showInfo_script)

    def getShortName(self, str):
        shortname = re.findall(r'[(](.*)[)]', str)
        return shortname[0] if shortname else ''

    def fliter(self, datalist):
        res_list = []
        for i in range(len(datalist)):
            flag = False
            if 'publication_title' in datalist[i]:
                for y in self.ccf_list:
                    shortname = self.getShortName(datalist[i]["publication_title"])
                    if datalist[i]["publication_title"].find(y[0]) != -1 or (shortname and y[1] and shortname == y[1]):
                        print(i,"success")
                        print([datalist[i]["publication_title"],shortname], '匹配' , y)
                        datalist[i]['match_longname'] = y[0] if y[0] else ''
                        datalist[i]['match_shortname'] = y[1] if y[1] else ''
                        res_list.append(datalist[i])
                        flag = True
                        break
                if not flag:
                    print(i,"fail")
                    print([datalist[i]["publication_title"],shortname], '匹配失败')
            else:
                print(i,"fail")
                print('该文章没有提供相应的出版物标题')
        return res_list

    def nextPage(self):
        try:
            next_btn = self.driver.find_element_by_css_selector('.next-btn')
            print('页码：', self.driver.find_element_by_css_selector('a.active').text)
            # next_btn.click()
            self.driver.execute_script("document.getElementsByClassName('next-btn')[0].getElementsByTagName('a')[0].click()")
            return True
        except Exception as e:
            print('已经到达最后一页（即找不到下一页的按钮了）：', e)
            return False

    def waitPage(self, delay):
        print('正在等待页面渲染成功...')
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "List-results")))
            print('List-results已加载')
        except Exception as e:
            print("获取论文列表超时", e)

        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "List-results-items")))
            print('List-results-items已加载')
        except Exception as e:
            try :
                print('List-results-items未加载')
                WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "List-results-message")))
                results_message = self.driver.execute_script("document.getElementsByClassName('List-results-message')[0].innerText;")
                print("查询列表为空，页面提示信息为：", results_message, '可能是网络问题，请重试或者检查url是否正确')
            except Exception as e:
                print("获取论文列表条目超时", e)

    def ReadPage(self):
        datalist = self.getInfo()
        print('本页条目数：' ,len(datalist))
        return datalist  
    
    def run(self, max = -1):
        #max为设置检索下限，检索成功的论文数不小于max
        print('开始检索文章：url：',self.url)
        start = timeit.default_timer()
        pTime(start)
        self.driver = webdriver.Chrome(options=self.brower_init())
        self.driver.get(self.url)
        self.waitPage(60)
        self.fliter(self.ReadPage())
        self.result = pandas.DataFrame(columns=("document_title","publication_title","url","authors","description","match_longname",'match_shortname',"abstract"))
        while self.nextPage() and (max == -1 or (max != -1 and len(self.result) < max)):
            self.waitPage(20)
            for row in self.fliter(self.ReadPage()):
                self.result = self.result.append(row, ignore_index=True) 
            pTime(start)
        print('检索结束，成功检索文章数：',len(self.result))
        self.driver.quit()
    
    def exportCSV(self, filename = './ieee导出结果.csv'):
        print('开始导出csv文件：',filename)
        self.result.to_csv(filename, columns=['document_title','publication_title','url','match_longname','match_shortname'])
        print('导出csv文件成功：',filename)
    
    
    def test_exportCSV(self, save_directory = '.'):
        now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        filename = save_directory + '/'+ now + '.csv'
        self.exportCSV(filename)
        
        
if __name__ == '__main__':
    save_directory = "E:/GraduationProject/result"
    test = 'https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=computer&highlight=true&returnType=SEARCH&matchPubs=true&pageNumber=130&returnFacets=ALL'

    ieee = IEEE(test, ccf_list)
    ieee.run()
    ieee.test_exportCSV(save_directory)
