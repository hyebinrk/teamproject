import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtWidgets,uic

# # Oracle 모듈
# import cx_Oracle as oci

## DB연결 설정
sid = 'XE'
host = 'localhost'
port = 1521
username = 'attendance'
password = '12345'
basic_msg = '출결관리앱'



class StudentloginWindow(QMainWindow):
    def __init__(self):
        super(StudentloginWindow, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./학생용출결체크.ui', self)
        self.setWindowTitle('학생용출결체크')
        # self.setWindowIcon(QIcon('./image/app01.png'))
        
        self.btn_my.clicked.connect(self.studentmyWindow)
        self.btn_atd.clicked.connect(self.atdcheckWindow)
        self.btn_eal.clicked.connect(self.atdcheckWindow)
        self.btn_cob.clicked.connect(self.atdcheckWindow)
        self.btn_out.clicked.connect(self.atdcheckWindow)
       
    def studentmyWindow(self):
        self.studentmypage_window = StudentMypageWindow()
        self.studentmypage_window.show()

    def atdcheckWindow(self):
        self.atdcheckpage_window = AtdCheckWindow()
        self.atdcheckpage_window.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = StudentloginWindow()
    win.show()
    app.exec_()
