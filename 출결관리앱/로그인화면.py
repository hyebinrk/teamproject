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

    
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
    
    def initUI(self):
        uic.loadUi('./teamproject/출결관리앱/로그인화면.ui', self)
        self.setWindowTitle('출결체크')
        # self.setWindowIcon(QIcon('./image/kitty.png'))
        
    # 버튼 이벤트 추가
        self.btnTeacherSelect.clicked.connect(self.btnTeacherClick)
        self.btnStudentSelect.clicked.connect(self.btnStudentClick)
        

    def btnTeacherClick(self):
        self.teacherlogin_window = TeacherloginWindow()
        self.teacherlogin_window.show()
        self.close()

    def btnStudentClick(self):
        self.studentlogin_window = StudentloginWindow()
        self.studentlogin_window.show()
        self.close()

class TeacherloginWindow(QMainWindow):
    def __init__(self):
        super(TeacherloginWindow, self).__init__()
        self.initUI()
        # self.loadData()
    
    def initUI(self):
        uic.loadUi('./teamproject/출결관리앱/t_login.ui', self)
        self.setWindowTitle('교사 로그인')

class StudentloginWindow(QMainWindow):
    def __init__(self):
        super(StudentloginWindow, self).__init__()
        self.initUI()
        # self.loadData()
    
    def initUI(self):
        uic.loadUi('./teamproject/출결관리앱/학생 로그인 화면.ui', self)
        self.setWindowTitle('학생 로그인')
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()