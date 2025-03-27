# 시스템 모듈 임포트
import sys
# PyQt5 위젯 및 GUI 관련 모듈 임포트
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtWidgets, uic

# Oracle 데이터베이스 연결을 위한 cx_Oracle 모듈 임포트
import cx_Oracle as oci



class TeacherAttcheck(QMainWindow):
    def __init__(self):
        super(TeacherAttcheck, self).__init__()
        self.initUI()
    
    def initUI(self):
        uic.loadUi('./teamproject/교사용 출석번호 출결체크.ui', self)
        self.setWindowTitle('(교사용)출석체크')
        # self.setWindowIcon(QIcon('./image/kitty.png'))
        self.show()

    def loadData(self):
        # db연결
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        query = '''SELECT S_NAME
	                FROM Students'''
        cursor.execute(query)

        # for i, item in enumerate(cursor, start=1):
        #     print(item)
        lst_student = [] # 리스트 생성
        for _, item in enumerate(cursor):
            lst_student.append(item)


        self.makeTable(lst_student) # 새로 생성한 리스트를 파라미터로 전달

        cursor.close()
        conn.close()
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    app.exec_()