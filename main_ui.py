from PyQt5.QtWidgets import *
from PyQt5.QtCore import (QObject, pyqtSignal, QEventLoop, QTimer,
                    QAbstractTableModel, Qt)
from PyQt5.QtGui import QTextCursor
import sys
import os
import threading
from time import ctime,sleep
import queue
import pandas as pd
import pyperclip # 剪切板
import webbrowser #浏览器
# 自己程序的api
from api import API

class EmittingStream(QObject):
    """Redirects console output to text widget."""
    newText = pyqtSignal(str)
 
    def write(self, text):
        self.newText.emit(str(text))
        
class pandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None
        
        

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
        # 重定向标准输出
        sys.stdout = EmittingStream(newText=self.onUpdateText)
        sys.stderr = EmittingStream(newText=self.onUpdateText)

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

    
    def ui1(self):
        frame = QFrame(self)
        
        verticalLayout = QVBoxLayout(frame)
        grid = QGridLayout()
        
        label_url = QLabel('检索网址：')
        url = "https://dl.acm.org/action/doSearch?AllField=machine+learning"
        self.lineEdit_url = QLineEdit(url)
        self.lineEdit_url.setPlaceholderText("请输入搜索地址(目前仅支持ieee与acm网站)：")
        
        label_cookie = QLabel('cookies：')
        #cookie = "SSO_IDP=https://idp.acm.org/idp/shibboleth; MAID=lIpCatIQKjCx5OdCfaIgfw==; I2KBRCK=1; _ga=GA1.2.236924004.1587806013; Pastease.passive.activated.5YhMrk04JDZQkJe=0; Pastease.passive.chance.5YhMrk04JDZQkJe=chance18.3; _hjid=d4f263a0-0eff-427c-8bf4-7870ebdf4a62; cookiePolicy=accept; PLUID=D1AxNpVcP6h10dGT/eK5BuKDO/E=; _gid=GA1.2.435292191.1589314560; __atuvc=1%7C19%2C19%7C20; SERVER=WZ6myaEXBLFWaYWZQ2cm9g==; MACHINE_LAST_SEEN=2020-05-14T09%3A00%3A35.345-07%3A00; _gat_UA-76155856-1=1; _hp2_ses_props.1083010732=%7B%22ts%22%3A1589472042590%2C%22d%22%3A%22dl.acm.org%22%2C%22h%22%3A%22%2Faction%2FdoSearch%22%2C%22q%22%3A%22%3FAllField%3Dmachine%2Blearning%22%7D; PU_LAST_LOGIN=2020-05-14T09%3A01%3A09.539-07%3A00; _hp2_id.1083010732=%7B%22userId%22%3A%227684480932003967%22%2C%22pageviewId%22%3A%227417895658108291%22%2C%22sessionId%22%3A%225380057420546304%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _gali=pb-page-content"
        self.lineEdit_cookie = QLineEdit()
        self.lineEdit_cookie.setPlaceholderText("输入cookie(如果不需要可以不加,cookie获取方式见文档)")
        verticalLayout.addWidget(self.lineEdit_cookie)
        
        label_num = QLabel('需要爬取文章数目：')
        self.lineEdit_num = QLineEdit(str(20))
        self.lineEdit_num.setPlaceholderText("输入爬取文章数目上限(为空表示无上限)")
        
        grid.addWidget(label_url, 0, 0)
        grid.addWidget(self.lineEdit_url, 0, 1)
        grid.addWidget(label_cookie, 1, 0)
        grid.addWidget(self.lineEdit_cookie, 1, 1)
        grid.addWidget(label_num, 2, 0)
        grid.addWidget(self.lineEdit_num, 2, 1)
        verticalLayout.addLayout(grid)
        
        self.headlessCheckBox = QCheckBox()#无头浏览器模式
        self.headlessCheckBox.setText('无头浏览器模式')
        verticalLayout.addWidget(self.headlessCheckBox)

        pushButton_enter = QPushButton()
        pushButton_enter.setText("搜索")
        pushButton_enter.clicked.connect(self.do_search)
        verticalLayout.addWidget(pushButton_enter)
        
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
        # 当前url
        self.nowUrlLabel = QLabel()
        self.nowUrlLabel.setWordWrap(True)
        self.nowUrlLabel.setAlignment(Qt.AlignTop)
        main_layout.addWidget(self.nowUrlLabel)
        
        pushButton_cls = QPushButton()
        pushButton_cls.setText("清空日志")
        pushButton_cls.clicked.connect(self.clearLog)
        main_layout.addWidget(pushButton_cls)
        
        # 日志，显示进度
        self.process = QTextEdit(self, readOnly=True)
        self.process.ensureCursorVisible()
        main_layout.addWidget(self.process) 

        main = QWidget()
        main.setLayout(main_layout)
        return main
        
    def ui3(self):
        main = QWidget()
        main_layout = QVBoxLayout()
        
        # 表格标题
        self.tableTitle = QLabel(main)
        self.tableTitle.setText('检索结果')
        main_layout.addWidget(self.tableTitle)
        
        self.tableWidget = QTableWidget()
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)#允许右键产生子菜单
        self.tableWidget.customContextMenuRequested.connect(self.generateMenu)#右键菜单
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        #self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setSortingEnabled(True)
        self.showResult('E:\\GraduationProject\\code_ui\\result\\test.csv')

        main_layout.addWidget(self.tableWidget)
        
        
        main.setLayout(main_layout)
        return main

    def ui4(self):
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel('page 4'))
        main_layout.addStretch(5)
        main = QWidget()
        main.setLayout(main_layout)
        return main
        
    def clearLog(self):
        self.process.clear()
        return
        
    def do_search(self):
        # 切换到日志界面
        self.right_widget.setCurrentIndex(1)
        
        print('检查参数')
        #此处理应详细检查输入参数
        try:
            self.url = self.lineEdit_url.text()
            self.cookie = self.lineEdit_cookie.text()
            self.num = int(self.lineEdit_num.text()) if self.lineEdit_num.text() else -1
            self.headless = self.headlessCheckBox.isChecked()
        except exception as e:
            print('输入格式有误', e)
        
        self.nowUrlLabel.setText(self.url)
        
        print('url:', self.url)
        print('cookie:', self.cookie)
        print('num:', self.num)
        print('headless:', self.headless)

        self.thread = threading.Thread(target=self.runThread)
        self.thread.start()

    def showResult(self, filename):
        self.df = pd.read_csv(filename)
        self.tableWidget.setColumnCount(len(self.df.columns))#设置列数
        self.tableWidget.setHorizontalHeaderLabels(list(self.df.columns))#设置表头文字
        
        for i in range(len(self.df)):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j in range(len(self.df.columns)):
                newItem = QTableWidgetItem(self.df.values[i][j])
                self.tableWidget.setItem(i, j, newItem)
    
    def runThread(self):
        print("开始线程", self.thread)
        self.result_filename = self.api.run(
            url = self.url, 
            cookie = self.cookie, 
            num = self.num,
            headless = self.headless,
            delay = 20)
        print("当前目录", os.getcwd())
        print("输出文件:", self.result_filename)
        
        # 切换到输出结果页面
        self.right_widget.setCurrentIndex(2)
        self.showResult(self.result_filename)
        
        print("线程结束", self.thread)
    
    def generateMenu(self, pos):
        ''' 右键菜单 '''
        row_num = self.tableWidget.currentRow()
        col_num = self.tableWidget.currentColumn()
        
        menu = QMenu()
        item1 = menu.addAction(u"复制")
        item2 = menu.addAction(u"在浏览器打开")
        item3 = menu.addAction(u"删除该行")
        action = menu.exec_(self.tableWidget.mapToGlobal(pos))
        if action == item1:
            text = self.tableWidget.item(row_num, col_num).text()
            #print('您复制了内容：', text)
            pyperclip.copy(text)
        elif action == item2:
            url = self.tableWidget.item(row_num, 2).text()
            webbrowser.open(url)
            #print('您在浏览器打开了：', )
        elif action == item3:
            self.tableWidget.removeRow(row_num)
            #print('您删除了：')
        else:
            return
            

api = None
if __name__ == '__main__':
    app = QApplication(sys.argv)
    api = API()
    ex = Window(api)#传递参数
    ex.show()
    sys.exit(app.exec_())