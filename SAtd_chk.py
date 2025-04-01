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
# host = 'localhost'  # 데이터베이스 호스트 주소 (외부 접속 시 변경 필요)
host = '210.119.14.71'
port = 1521  # 데이터베이스 포트 번호
username = 'attendance'  # 데이터베이스 사용자 이름
password = '12345'  # 데이터베이스 비밀번호
basic_msg = 'OO고등학교 출결관리앱 v1.0'

# 학생 로그인 > 출결체크 화면
class SAtdMainWindow(QMainWindow):
    def __init__(self, s_id=None):
        super(SAtdMainWindow, self).__init__()
        self.s_id = s_id # 로그인 클래스에서 전달받은 S_ID 저장 
        self.initUI()
        

    def initUI(self):
        uic.loadUi('./teamproject/SAtd_chk.ui', self)
        self.setWindowTitle('학생용출결체크')
        self.setWindowIcon(QIcon('./teamproject/image/app01.png'))
        
        self.btn_my.clicked.connect(self.MypageWindow)
        self.btn_atd.clicked.connect(self.MgmtAtdWindow)
        self.btn_eal.clicked.connect(self.btnEalClick)
        self.btn_cob.clicked.connect(self.btnCobClick)
        self.btn_out.clicked.connect(self.btnOutClick)
       
    def MypageWindow(self):
        from mypage import MypageWindow as MypageWindow  # 마이페이지.py에서 MypageWindow 가져오기
        self.my_page = MypageWindow()  # T_ID 전달
        self.my_page.show()  # 출결 체크 창 열기

    def MgmtAtdWindow(self):
        from AttendanceApp import AttendanceApp
        self.atd_mgmt = AttendanceApp()  # T_ID 전달
        self.atd_mgmt.show()


    
    def btnEalClick(self):
        """조퇴 버튼 클릭 시 DB 저장"""
        try:
            connection = oci.connect(username, password, f"{host}:{port}/{sid}")
            cursor = connection.cursor()

            cursor.execute("SELECT s_no FROM student WHERE s_id = :s_id", {"s_id": self.s_id})
            result = cursor.fetchone()

            if result:
                s_no = result[0]  # 학생 번호 가져오기

                query = """UPDATE atd
                        SET leave_time = CAST(SYSTIMESTAMP AT TIME ZONE 'UTC' AS TIMESTAMP WITH TIME ZONE) AT TIME ZONE 'Asia/Seoul'
                        WHERE s_no = :s_no
                        AND trunc(atd_date) = trunc(sysdate)"""
                

                cursor.execute(query, {"s_no": s_no})
                connection.commit()
                QMessageBox.information(self, "조퇴 처리 완료", "조퇴가 정상적으로 등록되었습니다.")
                # self.loadData()  # 데이터 새로고침
                
            else:
                QMessageBox.warning(self, "오류", "학생 정보를 찾을 수 없습니다.")
                print(f"s_id 값: {self.s_id}")


        except oci.DatabaseError as e:
            QMessageBox.critical(self, "데이터베이스 오류", f"오류 내용: {str(e)}")

        finally:
            cursor.close()
            connection.close()

        self.studentlogin_window = SAtdMainWindow()
        self.studentlogin_window.show()
        self.close()


    
    def btnOutClick(self):
        """외출 버튼 클릭 시 DB 저장"""
        try:
            connection = oci.connect(username, password, f"{host}:{port}/{sid}")
            cursor = connection.cursor()     

            cursor.execute("SELECT s_no FROM student WHERE s_id = :s_id", {"s_id": self.s_id})
            result = cursor.fetchone()   
            
            if result:
                s_no = result[0]  # s_no 값 추출

                query = """UPDATE atd
                        SET out_time = CAST(SYSTIMESTAMP AT TIME ZONE 'UTC' AS TIMESTAMP WITH TIME ZONE) AT TIME ZONE 'Asia/Seoul'
                        WHERE s_no = :s_no
                        AND trunc(atd_date) = trunc(sysdate)"""

                cursor.execute(query, {"s_no": s_no})
                connection.commit()
                QMessageBox.information(self, "알림", "외출이 정상 처리되었습니다.")
            else:
                QMessageBox.warning(self, "알림", "해당 학생을 찾을 수 없습니다.")    

        except oci.DatabaseError as e:
            QMessageBox.critical(self, "데이터베이스 오류", f"오류 내용: {str(e)}")

        finally:
            cursor.close()
            connection.close()
        
        self.studentlogin_window = SAtdMainWindow()
        self.studentlogin_window.show()
        self.close()


    def btnCobClick(self):
        """복귀 버튼 클릭 시 DB 저장"""
        try:
            connection = oci.connect(username, password, f"{host}:{port}/{sid}")
            cursor = connection.cursor()     

            cursor.execute("SELECT s_no FROM student WHERE s_id = :s_id", {"s_id": self.s_id})
            result = cursor.fetchone()   
            
            if result:
                s_no = result[0]  # s_no 값 추출

                query = """UPDATE atd
                        SET in_time = CAST(SYSTIMESTAMP AT TIME ZONE 'UTC' AS TIMESTAMP WITH TIME ZONE) AT TIME ZONE 'Asia/Seoul'
                        WHERE s_no = :s_no
                        AND trunc(out_time) = trunc(sysdate)"""

                cursor.execute(query, {"s_no": s_no})
                connection.commit()
                QMessageBox.information(self, "알림", "복귀가 정상 처리되었습니다.")
            else:
                QMessageBox.warning(self, "알림", "해당 학생을 찾을 수 없습니다.")    

        except oci.DatabaseError as e:
            QMessageBox.critical(self, "데이터베이스 오류", f"오류 내용: {str(e)}")

        finally:
            cursor.close()
            connection.close()

        self.studentlogin_window = SAtdMainWindow()
        self.studentlogin_window.show()
        self.close()

    


   

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SAtdMainWindow()
    win.show()
    app.exec_()