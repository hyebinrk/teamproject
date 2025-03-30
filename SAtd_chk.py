# 시스템 모듈 임포트
import sys

# PyQt5 위젯 및 GUI 관련 모듈 임포트
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtWidgets, uic

# Oracle 데이터베이스 연결을 위한 cx_Oracle 모듈 임포트
import cx_Oracle as oci

# Oracle 데이터베이스 연결 정보 설정
sid = 'XE'  # 데이터베이스 SID
host = 'localhost'  # 데이터베이스 호스트 주소 (외부 접속 시 변경 필요)
port = 1521  # 데이터베이스 포트 번호
username = 'attendance'  # 데이터베이스 사용자 이름
password = '12345'  # 데이터베이스 비밀번호
basic_msg = 'OO고등학교 출결관리앱 v1.0'

class SAtdMainWindow(QMainWindow):
    def __init__(self):
        super(SAtdMainWindow, self).__init__()
        self.S_ID = S_ID # 로그인 클래스에서 전달받은 S_ID 저장 
        self.initUI()

    def initUI(self):
        uic.loadUi('./학생용출결체크.ui', self)
        self.setWindowTitle('학생용출결체크')
        self.setWindowIcon(QIcon('./image/app01.png'))
        
        self.btn_my.clicked.connect(self.studentmyWindow)
        self.btn_atd.clicked.connect(self.atdcheckWindow)
        self.btn_eal.clicked.connect(self.btnEalClick)
        self.btn_cob.clicked.connect(self.atdcheckWindow)
        self.btn_out.clicked.connect(self.atdcheckWindow)
       
    def studentmyWindow(self):
        self.studentmypage_window = MypageWindow()
        self.studentmypage_window.show()

    def atdcheckWindow(self):
        self.atdcheckpage_window = AtdCheckWindow()
        self.atdcheckpage_window.show()

    def btnEalClick(self):
        """조퇴 버튼 클릭시 db저장"""
            
        try:
            connection = oci.connect(username, password, f"{host}:{port}/{sid}")
            cursor = connection.cursor()     

            cursor.execute("SELECT s_no FROM student WHERE s_id = :s_id", {"s_id": self.S_ID})
            result = cursor.fetchone()   
            
            if result:
                s_no = result[0] # s_no값 추출출
            
                query = """UPDATE atd
                            SET leave_time = SYSTIMESTAMP
                            WHERE s_no = 1
                            AND trunc(atd_date) = trunc(sysdate)"""

                cursor.execute(query, {
                    "1": s_no
                })
                connection.commit()
                QMessageBox.information(self, "지각 처리 되었습니다.")
                self.loadData()  # 데이터 새로고침
            else:
                print("해당 학생을 찾을 수 없습니다.")    

        except oci.DatabaseError as e:
            QMessageBox.critical(self, "데이터베이스 오류", f"오류 내용: {str(e)}")

        finally:
            cursor.close()
            connection.close()

        self.atdcheckpage_window = SAtdMainWindow()
        self.atdcheckpage_window.show()