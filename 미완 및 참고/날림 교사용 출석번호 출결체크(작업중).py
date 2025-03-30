# 시스템 모듈 임포트
import sys
# PyQt5 위젯 및 GUI 관련 모듈 임포트
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtWidgets, uic

# Oracle 데이터베이스 연결을 위한 cx_Oracle 모듈 임포트
import cx_Oracle as oci

sid = 'XE'
host = '210.119.14.71'
port = 1521
username = 'attendance'
password = '12345'

class TeacherEachAtdCheck(QMainWindow):
    def __init__(self, t_id, s_grade, s_class):
        super(TeacherEachAtdCheck, self).__init__()
        self.t_id = t_id            # login(관리자로그인).py 파일 속 클래스의 변수 값. (로그인 창에 입력한 교사 아이디)
        self.s_grade = s_grade      # 로그인 한 교사가 맡고 있는 학급의 학년 
        self.s_class = s_class      #로그인 한 교사가 맡고 있는 반
        self.initUI()
        self.StudentName()
    
    def initUI(self):
        uic.loadUi('./teamproject/교사용 출석번호 출결체크.ui', self)
        self.setWindowTitle('(교사용)출석체크')
        # self.setWindowIcon(QIcon('./image/kitty.png'))
        self.show()

    
    # 학년 이름 연결
    def SGrade(self):
        self.t_id.T_ID
        # db연결
        # conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        # cursor = conn.cursor()

        # query = '''SELECT S_BIRTH 
	    #             FROM Student'''
        # cursor.execute(query)




    
    # 반 이름 db연결 
    def SClassNo(self):
        # db연결
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        query = '''SELECT CLASS_NO 
	                FROM Student'''
        cursor.execute(query)


        # 결과 가져오기(리스트로 변환)
        class_no = [row[0] for row in cursor]

        cursor.close()
        conn.close()

        class_select = self.findChildren(label_5) 

        for checkbox, name in zip(checkboxes, student_names):
            checkbox.setText(name)
    
    
    # 학생이름 db연결 
    def StudentName(self):
        # db연결
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        query = '''SELECT S_NAME
	                FROM Student'''
        cursor.execute(query)


        # 결과 가져오기(리스트로 변환)
        student_names = [row[0] for row in cursor]

        cursor.close()
        conn.close()

        checkboxes = self.findChildren(QCheckBox) # Qt Designer에서 만든 체크박스 가져오기

        for checkbox, name in zip(checkboxes, student_names):
            checkbox.setText(name)

    
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TeacherEachAtdCheck()
    app.exec_()