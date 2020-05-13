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
            return driver.execute_script("return document.querySelector('{}') != undefined".format(self.element)) and driver.execute_script("return document.querySelector('{}') != null".format(self.element))
        elif self.locator == By.ID:
            return driver.execute_script("return document.getElementById('{}')[0] != undefined".format(self.element)) and driver.execute_script("return document.getElementById('{}')[0] != null".format(self.element))
        elif self.locator == By.TAG_NAME:
            return driver.execute_script("return document.getElementsByTagName('{}')[0] != undefined".format(self.element)) and driver.execute_script("return document.getElementsByTagName('{}')[0] != null".format(self.element))
        elif self.locator == 'js': #自行传入js脚本
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

    def matchSingleShortName(self, short, ccf_short):
        return short.strip().upper() == ccf_short.strip().upper()

    def hasShortName(self, publication_title):
        return ':' in publication_title
    
    def matchShortName(self, publication_title):
        regex = "([A-Za-z]+)(.*:)"
        pattern = re.compile(regex)
        res = pattern.match(publication_title)#match是从字符串最左端开始匹配，group(0)规定了是整个匹配结果，group(1)才是第一组 

        if not res:
            print('无简称')
            return True
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
        for th in self.ordinal[1:]:
            regex = "{}(.*)".format(th) #匹配序数词之后的  如'Proceedings of the 8th international'，匹配结果为' international'
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
        print('ccf_list：', len(ccf_list))
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
    
    
    