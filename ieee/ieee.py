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
    ordinal = ['', '1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th','11th','12th','13th','14th','15th','16th','17th','18th','19th','20th','21st','22nd','23rd','24th']
    
    
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

    def matchSingleShortName(self, short, ccf_short):
        return short.strip().upper() == ccf_short.strip().upper()

    def hasShortName(self, publication_title):
        return '(' in publication_title

    def matchShortName(self, publication_title):
        regex = r'[(](.*)[)]'
        pattern = re.compile(regex)
        res = pattern.search(publication_title)#注意是'search'，与acm的不同，group(1)才是第一组 

        if not res:
            print('无简称')
            return False
        else:
            short = res.group(1)
            for y in self.ccf_list:
                ccf_short = y[1]
                if not ccf_short:
                    continue
                if self.matchSingleShortName(short, ccf_short):
                    print('有简称且匹配成功:', [short, ccf_short])
                    self.match_ccf = y
                    return True
            print('有简称但匹配失败', [short])
            return False

    def matchSingleLongName(self, long, ccf_long):
        ccf_long_after = re.sub("^[A-Za-z]* ", '', ccf_long, count=1).strip().upper()
        long = long.strip().upper()
        return long == ccf_long or long == ccf_long_after

    def matchLongName(self, publication_title):
        long = publication_title
        # 去掉年份
        long = re.sub("^[0-9]+ ", '', long, count=1)# 注意年份后有空格
        # 取序数词之后的  如'Proceedings of the 8th international...'，取' international...'
        for th in self.ordinal[1:]:
            regex = "{}(.*)".format(th) 
            pattern = re.compile(regex)
            res = pattern.search(publication_title)
            if res:
                long = res.group(1).strip().upper()
                break

        for y in self.ccf_list:
            ccf_long = y[0]
            if self.matchSingleLongName(long, ccf_long):
                print('全称匹配成功:', [publication_title,ccf_long])
                self.match_ccf = y
                return True
        print('匹配失败',publication_title)
        return False


    def check(self, publication_title):
        if self.hasShortName(publication_title):
            return self.matchShortName(publication_title)
        elif self.matchLongName(publication_title):
            return True
        else:
            return False 
        
    def fliter(self, pageList):
        print('ccf_list：', len(self.ccf_list))
        res_list = []
        for i in range(len(pageList)):
            if 'publication_title' in pageList[i]:
                if self.check(pageList[i]["publication_title"]):
                    print(i,"success\n")
                    pageList[i]['match_longname'] = self.match_ccf[0] if self.match_ccf[0] else ''
                    pageList[i]['match_shortname'] = self.match_ccf[1] if self.match_ccf[1] else ''
                    res_list.append(pageList[i])
                else:
                    print(i,"fail\n")
                    #print(pageList[i]["publication_title"], '匹配失败')
            else:
                print('该文章没有提供相应的出版物标题')
                print(i,"fail\n")
        return res_list

    def nextPage(self):
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "next-btn")))
            print('页码：', self.driver.execute_script("return document.querySelector('a.active').innerText"))
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
        #self.driver.get(self.url)
        self.driver.execute_script("window.location.href = '{}'".format(self.url))
        self.waitPage(60)
        self.fliter(self.ReadPage())
        self.result = pandas.DataFrame(columns=("document_title","publication_title","url","authors","description","match_longname",'match_shortname',"abstract"))
        while self.nextPage() and (max == -1 or (max != -1 and len(self.result) < max)):
            self.waitPage(20)
            for row in self.fliter(self.ReadPage()):
                self.result = self.result.append(row, ignore_index=True) 
            pTime(start)
            print('已经成功检索文章：',len(self.result))
        print('检索结束，成功检索文章数：',len(self.result))
        self.driver.quit()
    
    def exportCSV_byFilename(self, filename = './ieee导出结果.csv'):
        print('开始导出csv文件：',filename)
        self.result.to_csv(filename, columns=['document_title','publication_title','url','match_longname','match_shortname'])
        print('导出csv文件成功：',filename)
    
    
    def exportCSV_byFilefolder(self, directory = '.'):
        now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        filename = directory + '/'+ now + '.csv'
        self.exportCSV_byFilename(filename)
        
