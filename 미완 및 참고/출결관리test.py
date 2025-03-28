import sys
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi

# DB 연결 설정
sid = 'XE'
host = 'localhost'
port = 1521
username = 'attendance'
password = '12345'
basic_msg = '출결관리앱'

class TeacherloginWindow(QMainWindow):
    def __init__(self):
        super(TeacherloginWindow, self).__init__()
        self.initUI()
    
    def initUI(self):
        uic.loadUi('./teamproject/login(교사로그인)/t_login.ui', self)
        self.setWindowTitle('교사 로그인')

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
    
    def initUI(self):
        uic.loadUi('./teamproject/로그인화면.ui', self)
        self.setWindowTitle('출결체크')

        # ✅ 직접 접근 (findChild 필요 없음)
        self.btnTeacherSelect.clicked.connect(self.btnTeacherClick)

    def btnTeacherClick(self):
        print("✅ 교사 로그인 창 열기")
        self.teacher_window = TeacherloginWindow()
        self.teacher_window.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())