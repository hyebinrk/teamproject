import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5 import uic
from PyQt5.QtGui import QPixmap  # QPixmap 모듈 추가

# Oracle 데이터베이스 연결을 위한 cx_Oracle 모듈 임포트
import cx_Oracle as oci

# Oracle 데이터베이스 연결 정보 설정
sid = 'XE'  # 데이터베이스 SID
host = '210.119.14.71'  # 데이터베이스 호스트 주소 (외부 접속 시 변경 필요)
port = 1521  # 데이터베이스 포트 번호
username = 'attendance'  # 데이터베이스 사용자 이름
password = '12345'  # 데이터베이스 비밀번호

# 메인 윈도우 클래스 정의
class MainWindow(QMainWindow): 
    def __init__(self):
        super(MainWindow, self).__init__() 
        self.initUI()  # UI 초기화 함수 호출
        self.generated_numbers = set()  # 생성된 숫자를 저장할 집합 초기화

    # UI 초기화 함수
    def initUI(self):
        # UI 파일 로드
        uic.loadUi('./teamproject/loginway.ui', self)
        self.setWindowTitle('학생용 로그인 방식')  # 윈도우 제목 설정
        

         # QLabel 객체 가져오기
        self.atd_num_label = self.findChild(QLabel, 'atd_num')
        self.images_label = self.findChild(QLabel, 'images') 
        self.images_2_label = self.findChild(QLabel, 'images_2') 

        # QLabel에 이미지 설정
        pixmap = QPixmap('./teamproject/images/mypage.png')  # 이미지 파일 경로
        self.images_label.setPixmap(pixmap)  # QLabel에 이미지 설정
        self.images_label.setScaledContents(True)  # 이미지가 QLabel 크기에 맞게 조정되도록 설정

        pixmap = QPixmap('./teamproject/images/atd.png')  # 이미지 파일 경로
        self.images_2_label.setPixmap(pixmap)  # QLabel에 이미지 설정
        self.images_2_label.setScaledContents(True)  # 이미지가 QLabel 크기에 맞게 조정되도록 설정

        # 출결번호 생성 버튼 클릭 시그널 연결
        self.btn_num.clicked.connect(self.btnchkClick)

        # 랜덤 숫자 데이터 삭제 버튼 클릭 시그널 연결
        self.btn_clear = self.findChild(QPushButton, 'btn_clear')  # QPushButton ID가 'btn_clear'인 위젯 가져오기
        self.btn_clear.clicked.connect(self.clearRandomNumbers)

    # btn_chk 버튼 클릭 이벤트 처리 함수
    def btnchkClick(self):
        # 중복되지 않은 랜덤 숫자 생성
        if len(self.generated_numbers) >= 100:
            QMessageBox.warning(self, '경고', '모든 숫자가 생성되었습니다!')
            return
        while True:
            random_number = random.randint(1, 100)
            if random_number not in self.generated_numbers:
                self.generated_numbers.add(random_number)
                break

        # 데이터베이스에 랜덤 숫자 저장
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()
        try:
            # TEACHER와 ATD 테이블에서 T_NO가 같은 S_NO에게 CHECKNO 부여
            query = '''
                UPDATE ATD
                   SET CHECKNO = :random_number
                 WHERE S_NO IN (
                       SELECT S_NO
                         FROM TEACHER
                        WHERE T_NO = ATD.T_NO
                   )
            '''
            cursor.execute(query, {'random_number': random_number})
            conn.commit()
            QMessageBox.information(self, '성공', f'출석번호 {random_number}이(가) 저장되었습니다.')
        except Exception as e:
            QMessageBox.critical(self, '오류', f'데이터베이스 오류: {e}')
        finally:
            cursor.close()
            conn.close()

        # 생성된 랜덤 숫자를 QLabel에 표시
        self.atd_num_label.setText(str(random_number))

    # 랜덤 숫자 데이터 삭제 버튼 클릭 이벤트 처리 함수
    def clearRandomNumbers(self):
        # 데이터베이스에서 CHECKNO 초기화
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()
        try:
            query = 'UPDATE ATD SET CHECKNO = NULL'
            cursor.execute(query)
            conn.commit()
            QMessageBox.information(self, '성공', '모든 출석번호가 초기화되었습니다.')
        except Exception as e:
            QMessageBox.critical(self, '오류', f'데이터베이스 오류: {e}')
        finally:
            cursor.close()
            conn.close()

        # 생성된 숫자 집합 초기화
        self.generated_numbers.clear()
        self.atd_num_label.setText('')  # QLabel 초기화

        # 프로그램 실행 진입점
if __name__ == '__main__':
    app = QApplication(sys.argv)  # QApplication 객체 생성
    win = MainWindow()  # MainWindow 객체 생성
    win.show()  # 메인 윈도우 표시
    app.exec_()  # 이벤트 루프 실행