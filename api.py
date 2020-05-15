from ccf.ccf import CCF
from ieee.ieee import IEEE
from acm.acm import ACM
import os

ieee_web = 'ieeexplore.ieee.org'
acm_web = 'dl.acm.org'

class API():
    def __init__(self):
        # 获取ccf目录
        ccf = CCF()
        self.ccf_list = ccf.run()

    def initArgv(self, url, cookie, num, headless=False, delay=20):
        if 'https://' not in url:
            url = 'https://' + url
        self.url = url
        self.cookie = cookie
        self.num = num
        self.headless = headless
        self.delay = delay
        # 判断论文网站
        if ieee_web in self.url:
            self.paper_crawler = IEEE(self.url, self.ccf_list)
        elif acm_web in self.url:
            self.paper_crawler = ACM(self.url, self.ccf_list)
        # 设置属性
        self.paper_crawler.setHeadless(headless)
        if cookie:
            self.paper_crawler.setCookie(cookie)
        if num:
            self.paper_crawler.setNum(num)
        if delay:
            self.paper_crawler.setDelay(delay)
        

    def run(self, url, num, cookie=None, headless=False, delay=20):
        self.initArgv(url, cookie, num, headless, delay)
        self.paper_crawler.run()
        return self.paper_crawler.exportCSV_byFilefolder("./result")



