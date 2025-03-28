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

class MypageWindow(QDialog):
    def __init__(self):
        super(MypageWindow, self).__init__()
        self.initUI()
    
    def initUI(self):
        uic.loadUi('./teamproject/마이페이지.ui', self)
        self.setWindowTitle('마이페이지')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MypageWindow()
    win.show()
    app.exec_()