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


class js_element_has_element(object):
    """
    利用js代码来检查元素是否存在
    """
    def __init__(self, locator):
        self.locator = locator[0]
        self.element = locator[1]

    def __call__(self, driver):
        if self.locator == By.CLASS_NAME:
            return driver.execute_script("return document.getElementsByClassName('{}')[0] != undefined".format(self.element)) and driver.execute_script("return document.getElementsByClassName('{}')[0] != null".format(self.element))
        elif self.locator == By.CSS_SELECTOR :
            #return driver.execute_script("return document.querySelector('{}') != null".format(self.element))
            return driver.execute_script("return document.querySelector('{}') != undefined".format(self.element)) and driver.execute_script("return document.querySelector('{}') != null".format(self.element))
        elif self.locator == By.ID:
            #return driver.execute_script("return document.getElementById('{}')[0] != null".format(self.element))
            return driver.execute_script("return document.getElementById('{}')[0] != undefined".format(self.element)) and driver.execute_script("return document.getElementById('{}')[0] != null".format(self.element))
        elif self.locator == By.TAG_NAME:
            #return driver.execute_script("return document.getElementsByTagName('{}')[0] != null".format(self.element))
            return driver.execute_script("return document.getElementsByTagName('{}')[0] != undefined".format(self.element)) and driver.execute_script("return document.getElementsByTagName('{}')[0] != null".format(self.element))
        elif self.locator == 'js': #自行传入js脚本
            #return driver.execute_script("return {} != null".format(self.element))
            return driver.execute_script("return {} != undefined".format(self.element)) and driver.execute_script("return document.getElementsByTagName('{}')[0] != null".format(self.element))
        else :
            print('js中不存在该类型的定位器', self.locator)
            return False

class ACM:
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
        # chrome_options.add_argument('--disable-gpu')  # 如果不加这个选项，有时定位会出现问题
        return chrome_options

    def getInfo(self):
        showInfo_script = showInfo_script = "\
        function showInfo(node){\
            var paper_info = {};\
            try {\
                home = 'https://dl.acm.org';\
                paper_info['document_title'] = node.querySelector('.issue-item__title .hlFld-Title').innerText;\
                paper_info['url'] = home + node.getElementsByClassName('hlFld-Title')[0].getElementsByTagName('a')[0].getAttribute('href');\
                paper_info['description'] = [];\
                node.querySelectorAll('.issue-item__detail .dot-separator span').forEach((x) => paper_info['description'].push(x.innerText));\
                link = node.querySelector('.issue-item__detail a').href;\
                paper_info['publication_title'] = node.querySelector('.issue-item__detail a').getAttribute('title');\
                paper_info['abstract'] = node.querySelector('.issue-item__abstract').innerText;        \
            }catch(err) {                                                                   \
                console.log('%c该节点获取信息有误（可能有部分信息缺失）', err ,'color:blue;font-size:15px');\
                console.log(err);\
                console.log(node);                                                                 \
            }                                                                                      \
            console.log('文章标题:'		 + paper_info['document_title']);                            \
            console.log('出版物标题：'	 + paper_info['publication_title']);                       \
            console.log('文章说明：'          + paper_info['description']);                        \
            console.log('url：'          + paper_info['url']);                                     \
            console.log('摘要：'       + paper_info['abstract']);     \
            return paper_info;                                                                     \
        }\
        function getInfoList(){                                                                    \
            infoList = [];                                                                         \
            list = document.getElementsByClassName('search__item');                                \
            for (var i = 0; i < list.length; i++) {                                                \
                console.log(i);                                                                    \
                console.log(list[i]);                                                              \
                infoList.push(showInfo(list[i]));                                                  \
            }                                                                                      \
            return infoList;                                                                       \
        }\
        return getInfoList();"
        return self.driver.execute_script(showInfo_script)

    def check(self, longname, ccf_shortname, ccf_longname):
        return longname == ccf_longname

    def fliter(self, pageList):
        res_list = []
        for i in range(len(pageList)):
            isMatch = False
            if 'publication_title' in pageList[i]:
                for y in self.ccf_list:
                    if self.check(pageList[i]["publication_title"], y[0], y[1]):
                        # 打印信息
                        print(i,"success")
                        print(pageList[i]["publication_title"], '匹配' , y)
                        # 填充信息
                        pageList[i]['match_longname'] = y[0] if y[0] else ''
                        pageList[i]['match_shortname'] = y[1] if y[1] else ''
                        # 添加进结果
                        res_list.append(pageList[i])
                        # 跳出循环
                        isMatch = True
                        break
                if not isMatch:
                    print(i,"fail")
                    print(pageList[i]["publication_title"], '匹配失败')
            else:
                print(i,"fail")
                print('该文章没有提供相应的出版物标题')
        return res_list

    def nextPage(self, delay):
        # 下一页
        print('\n正在跳转下一页')
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "pagination__btn--next")))
            WebDriverWait(self.driver, delay).until(js_element_has_element((By.CLASS_NAME, "pagination__btn--next")))
            next_url = self.driver.execute_script("return document.getElementsByClassName('pagination__btn--next')[0].href")
            #打开下一页
            #self.driver.get(next_url)
            self.driver.execute_script("window.location.href = '{}'".format(next_url))
            try:
                #当前页码
                WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".pagination__list .active")))
                WebDriverWait(self.driver, delay).until(js_element_has_element((By.CSS_SELECTOR, ".pagination__list .active")))
                print('当前页页码：', self.driver.execute_script("return document.querySelector('.pagination__list .active').innerText"))
            except Exception as e:
                print('获取当前页码失败：', e)
                return True
        except Exception as e:
            try:
                WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "search-result__no-result")))
                print('已经到达最后一页了：', self.driver.execute_script("return document.getElementsByClassName('search-result__no-result')[0].innerText"))
            except Exception as e2:
                print('下一页跳转失败，可能是网络问题：', e)
            return False
        return True


    def waitPage(self, delay):
        print('正在等待页面渲染成功...')
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "items-results")))
            WebDriverWait(self.driver, delay).until(js_element_has_element((By.CLASS_NAME, "items-results")))
            print('items-results已加载')
        except Exception as e:
            print("获取论文列表超时", e)

        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "search__item")))
            WebDriverWait(self.driver, delay).until(js_element_has_element((By.CLASS_NAME, "search__item")))
            print('search__item已加载')
        except Exception as e:
            try :
                print('search__item未加载')
                WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "search-result__no-result")))
                WebDriverWait(self.driver, delay).until(js_element_has_element((By.CLASS_NAME, "search-result__no-result")))
                results_message = self.driver.execute_script("document.getElementsByClassName('search-result__no-result')[0].innerText;")
                print("查询列表为空，页面提示信息为：", results_message)
            except Exception as e:
                print("获取论文列表条目超时,可能是网络问题，请重试或者检查url是否正确", e)
        
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, "pagination__list")))
            WebDriverWait(self.driver, delay).until(js_element_has_element((By.CLASS_NAME, "pagination__list")))
            print('pagination__list已加载')
        except Exception as e:
            print("获取页码超时", e)
            

    def ReadPage(self):
        pageList = self.getInfo()
        print('本页条目数：' ,len(pageList))
        return pageList
    
    def run(self, max = -1):
        #max为设置检索下限，检索成功的论文数不小于max
        print('开始检索文章：url：',self.url)
        start = timeit.default_timer()
        pTime(start)
        self.driver = webdriver.Chrome(options=self.brower_init())
        print('正在打开网页')
        self.driver.execute_script("window.location.href = '{}'".format(self.url))
        # self.driver.get(self.url)
        self.waitPage(60)
        self.fliter(self.ReadPage())
        self.result = pandas.DataFrame(columns=("document_title","publication_title","url","authors","description","match_longname",'match_shortname',"abstract"))
        while self.nextPage(20) and (max == -1 or (max != -1 and len(self.result) < max)):
            self.waitPage(20)
            for row in self.fliter(self.ReadPage()):
                self.result = self.result.append(row, ignore_index=True)
            pTime(start)
        print('检索结束，成功检索文章数：',len(self.result))
        self.driver.quit()
    
    def exportCSV(self, filename = './ccf导出结果.csv'):
        print('开始导出csv文件：',filename)
        self.result.to_csv(filename, columns=['document_title','publication_title','url','match_longname','match_shortname'])
        print('导出csv文件成功：',filename)
    
    
    def test_exportCSV(self, save_directory = '.'):
        now = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        filename = save_directory + '/'+ now + '.csv'
        self.exportCSV(filename)
        
    def test(self):
        print('开始检索文章：url：',self.url)
        start = timeit.default_timer()
        pTime(start)
        self.driver = webdriver.Chrome(options=self.brower_init())
        self.driver.get(self.url)
        
        
if __name__ == '__main__':
    save_directory = "."
    url = 'https://dl.acm.org/action/doSearch?AllField=machine+learning&pageSize=50'
    
    acm = ACM(url, ccf_list)
    acm.run(0)
    ieee.test_exportCSV(save_directory)
    
    
    