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
host = '210.119.14.71'  # 데이터베이스 호스트 주소 (외부 접속 시 변경 필요)
port = 1521  # 데이터베이스 포트 번호
username = 'attendance'  # 데이터베이스 사용자 이름
password = '12345'  # 데이터베이스 비밀번호

# 메인 윈도우 클래스 정의
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()  # UI 초기화 함수 호출

    # UI 초기화 함수
    def initUI(self):
        # UI 파일 로드
        uic.loadUi('./teamproject/t_login.ui', self)
        self.setWindowTitle('교사용 로그인')  # 윈도우 제목 설정

        # 로그인 버튼 클릭 시그널 연결
        self.btn_login.clicked.connect(self.btnAddClick)

    # 입력 필드 초기화 함수
    def clearInput(self):
        self.input_T_ID.clear()  # 아이디 입력 필드 초기화
        self.input_T_PW.clear()  # 비밀번호 입력 필드 초기화

    # 로그인 버튼 클릭 이벤트 처리 함수
    def btnAddClick(self):
        # 입력 필드에서 아이디와 비밀번호 값 가져오기
        T_ID = self.input_T_ID.text()
        T_PW = self.input_T_PW.text()

        # 입력값 검증 (Validation Check)
        if T_ID == '' or T_PW == '':
            # 입력값이 비어있을 경우 경고 메시지 표시
            QMessageBox.warning(self, '경고', '아이디,비밀번호 입력은 필수 입니다!')
            return  # 함수 종료
        else:
            print('로그인 진행!') 
            values = (T_ID, T_PW)  # 입력값을 튜플로 저장
            # 데이터베이스에서 로그인 정보 확인
            if self.addData(values) == True:  # 로그인 성공
                QMessageBox.about(self, '로그인 성공!', '선생님 어서오세요! ')
            else:  # 로그인 실패
                QMessageBox.about(self, '로그인 실패!', '로그인 실패, 관리자에게 문의하세요.')
        self.clearInput()  # 입력 필드 초기화

    # 데이터베이스에서 로그인 정보 확인 함수
    def addData(self, values):
        isSucceed = False  # 로그인 성공 여부 초기화
        # 데이터베이스 연결
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()  # 커서 객체 생성

        try:
            # 로그인 정보 확인 쿼리
            query = '''
                    SELECT COUNT(*)
                      FROM TEACHER
                     WHERE T_ID = :v_T_ID
                       AND T_PW = :v_T_PW
                    '''
            # 쿼리 실행 (바인딩 변수 사용)
            cursor.execute(query, {'v_T_ID': values[0], 'v_T_PW': values[1]})
            result = cursor.fetchone()  # 결과 가져오기

            # 결과가 0보다 크면 로그인 성공
            if result[0] > 0:
                isSucceed = True
        except Exception as e:
            # 예외 발생 시 오류 메시지 출력
            print(f"❌ 오류 발생: {e}")
        finally:
            # 커서와 연결 종료
            cursor.close()
            conn.close()

        return isSucceed  # 로그인 성공 여부 반환
    
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()  # UI 초기화 함수 호출
        self.generated_numbers = set()  # 생성된 숫자를 저장할 집합 초기화

    # UI 초기화 함수
    def initUI(self):
        # UI 파일 로드
        uic.loadUi('./teamproject/atd_chk.ui', self)
        self.setWindowTitle('교사용 출결체크')  # 윈도우 제목 설정

        # QLabel 객체 가져오기
        self.num_chk_label = self.findChild(QLabel, 'num_chk')  # QLabel ID가 'num_chk'인 위젯 가져오기
        self.my_page_label = self.findChild(QLabel, 'my_page')  # QLabel ID가 'image_label'인 위젯 가져오기
        self.my_atd_label = self.findChild(QLabel, 'my_atd')  # QLabel ID가 'image_label'인 위젯 가져오기

        # QLabel에 이미지 설정
        pixmap = QPixmap('./teamproject/images/mypage.png')  # 이미지 파일 경로
        self.my_page_label.setPixmap(pixmap)  # QLabel에 이미지 설정
        self.my_page_label.setScaledContents(True)  # 이미지가 QLabel 크기에 맞게 조정되도록 설정

        pixmap = QPixmap('./teamproject/images/atd.png')  # 이미지 파일 경로
        self.my_atd_label.setPixmap(pixmap)  # QLabel에 이미지 설정
        self.my_atd_label.setScaledContents(True)  # 이미지가 QLabel 크기에 맞게 조정되도록 설정

        # 출결번호 생성 버튼 클릭 시그널 연결
        self.btn_chk.clicked.connect(self.btnchkClick)

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
        # 생성된 랜덤 숫자를 QLabel에 표시
        self.num_chk_label.setText(str(random_number))

# 프로그램 실행 진입점
if __name__ == '__main__':
    app = QApplication(sys.argv)  # QApplication 객체 생성
    win = MainWindow()  # MainWindow 객체 생성
    win.show()  # 메인 윈도우 표시
    app.exec_()  # 이벤트 루프 실행