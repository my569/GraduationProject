from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, pyqtSignal, QEventLoop, QTimer
from PyQt5.QtGui import QTextCursor
import sys
from api import API
import threading
from time import ctime,sleep
import queue


class EmittingStream(QObject):
    """Redirects console output to text widget."""
    newText = pyqtSignal(str)
 
    def write(self, text):
        self.newText.emit(str(text))

class Window(QMainWindow):
    def __init__(self, api):
        super().__init__()
        
        # 代码api
        self.api = api
        # 线程队列
        q = queue.Queue()

        # 标题
        self.setWindowTitle('CS高质量论文检索工具')

        # 窗口大小
        self.Width = 800
        self.height = int(0.618 * self.Width)
        self.resize(self.Width, self.height)
		
		# 生成按钮
        self.btn_1 = QPushButton('搜索', self)
        self.btn_2 = QPushButton('日志', self)
        self.btn_3 = QPushButton('输出结果', self)
        self.btn_4 = QPushButton('会议分布', self)

        # 绑定按钮点击事件
        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        self.btn_4.clicked.connect(self.button4)

        # 右侧窗体的内容
        self.tab1 = self.ui1()
        self.tab2 = self.ui2()
        self.tab3 = self.ui3()
        self.tab4 = self.ui4()

        self.initUI()
        # Custom output stream.
        sys.stdout = EmittingStream(newText=self.onUpdateText)

    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.process.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()


    def initUI(self):
        # 左侧布局
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        left_layout.addWidget(self.btn_4)
        left_layout.addStretch(5)
        left_layout.setSpacing(20)
        self.left_widget = QWidget() #左侧
        self.left_widget.setLayout(left_layout)

        # 右侧内容为一个QTabWidget控件
        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")

        self.right_widget.addTab(self.tab1, '')
        self.right_widget.addTab(self.tab2, '')
        self.right_widget.addTab(self.tab3, '')
        self.right_widget.addTab(self.tab4, '')

        self.right_widget.setCurrentIndex(0)
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; \
            height: 0; margin: 0; padding: 0; border: none;}''')

        # 整体布局
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    # ----------------- 
    # buttons

    def button1(self):
        self.right_widget.setCurrentIndex(0)

    def button2(self):
        self.right_widget.setCurrentIndex(1)

    def button3(self):
        self.right_widget.setCurrentIndex(2)

    def button4(self):
        self.right_widget.setCurrentIndex(3)
	
	# ----------------- 
    # pages

    def ui1(self):
        frame = QFrame(self)
        verticalLayout = QVBoxLayout(frame)

        url = "https://dl.acm.org/action/doSearch?AllField=machine+learning"
        self.lineEdit_url = QLineEdit(url)
        self.lineEdit_url.setPlaceholderText("请输入搜索地址(目前仅支持ieee与acm网站)：")
        verticalLayout.addWidget(self.lineEdit_url)
        
        cookie = "SSO_IDP=https://idp.acm.org/idp/shibboleth; MAID=lIpCatIQKjCx5OdCfaIgfw==; I2KBRCK=1; _ga=GA1.2.236924004.1587806013; Pastease.passive.activated.5YhMrk04JDZQkJe=0; Pastease.passive.chance.5YhMrk04JDZQkJe=chance18.3; _hjid=d4f263a0-0eff-427c-8bf4-7870ebdf4a62; cookiePolicy=accept; PLUID=D1AxNpVcP6h10dGT/eK5BuKDO/E=; _gid=GA1.2.435292191.1589314560; __atuvc=1%7C19%2C19%7C20; SERVER=WZ6myaEXBLFWaYWZQ2cm9g==; MACHINE_LAST_SEEN=2020-05-14T09%3A00%3A35.345-07%3A00; _gat_UA-76155856-1=1; _hp2_ses_props.1083010732=%7B%22ts%22%3A1589472042590%2C%22d%22%3A%22dl.acm.org%22%2C%22h%22%3A%22%2Faction%2FdoSearch%22%2C%22q%22%3A%22%3FAllField%3Dmachine%2Blearning%22%7D; PU_LAST_LOGIN=2020-05-14T09%3A01%3A09.539-07%3A00; _hp2_id.1083010732=%7B%22userId%22%3A%227684480932003967%22%2C%22pageviewId%22%3A%227417895658108291%22%2C%22sessionId%22%3A%225380057420546304%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _gali=pb-page-content"
        self.lineEdit_cookie = QLineEdit(cookie)
        self.lineEdit_cookie.setPlaceholderText("输入cookie(如果不需要可以不加,cookie获取方式见文档)")
        verticalLayout.addWidget(self.lineEdit_cookie)
        
        num = 20
        self.lineEdit_num = QLineEdit(str(num))
        self.lineEdit_num.setPlaceholderText("输入爬取文章数目上限(为空表示无上限)")
        verticalLayout.addWidget(self.lineEdit_num)
        
        self.headlessCheckBox = QCheckBox()#无头浏览器模式
        self.headlessCheckBox.setText('无头浏览器模式')
        verticalLayout.addWidget(self.headlessCheckBox)

        pushButton_enter = QPushButton()
        pushButton_enter.setText("搜索")
        pushButton_enter.clicked.connect(self.do_search)
        # pushButton_enter.clicked.connect(selof.genMastClicked)
        verticalLayout.addWidget(pushButton_enter)
        
        # Create the text output widget.
        self.process = QTextEdit(self, readOnly=True)
        self.process.ensureCursorVisible()
        self.process.setLineWrapColumnOrWidth(500)
        self.process.setLineWrapMode(QTextEdit.FixedPixelWidth)
        self.process.setFixedWidth(400)
        self.process.setFixedHeight(200)
        self.process.move(30, 50)
        verticalLayout.addWidget(self.process)
        # self.process.ensureCursorVisible()
        # self.process.setLineWrapColumnOrWidth(500)
        # self.process.setLineWrapMode(QTextEdit.FixedPixelWidth)
        # self.process.setFixedWidth(400)
        # self.process.setFixedHeight(200)
        # self.process.move(30, 50)
        
        
        
        # 添加空白
        verticalLayout.addStretch(1000)
        #左下角状态栏
        self.statusBar()
        self.statusBar().showMessage('状态栏')
        
        main = QWidget()
        main.setLayout(verticalLayout)
        
        return main

    def ui2(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 2'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main
        
    def ui3(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 3'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main

    def ui4(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 4'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main
        
    def printhello(self):
        print('hello')
        
    def do_search(self):
        print('检查参数')
        #此处理应详细检查输入参数
        try:
            self.url = self.lineEdit_url.text()
            self.cookie = self.lineEdit_url.text()
            self.num = int(self.lineEdit_num.text())
            self.headless = self.headlessCheckBox.isChecked()
        except exception as e:
            print('输入格式有误', e)
            
        test = 'https://ieeexplore.ieee.org/search/searchresult.jsp?queryText=machine%20learning&highlight=true&returnType=SEARCH&matchPubs=true&ranges=2000_2020_Year&returnFacets=ALL&refinements=ContentType:Conferences'
        print('url:', self.url)
        print('cookie:', self.cookie)
        print('num:', self.num)
        print('headless:', self.headless)
        self.thread = threading.Thread(target=self.runThread)
        self.thread.start()
        # if q.empty():
            # addSearch()
            # self.thread = threading.Thread(target=self.runThread)
            # self.thread.start()
        # else:
            # q.put(t)
        
        
    # def addSearch():
        # #入队列
        # q.put()
        # #加记录
        
        
    # def finishSearch()
        # #出队列
        # #标记搜索完成
        # 如果不为空就
            # return True
        
    def runThread(self):
        print("开始线程", self.thread)
        self.api.run(url=self.url, cookie=self.cookie, num=self.num)
        print("线程结束", self.thread)
        

api = None
if __name__ == '__main__':
    api = API()
    app = QApplication(sys.argv)
    ex = Window(api)#传递参数
    ex.show()
    sys.exit(app.exec_())