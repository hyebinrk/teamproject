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
basic_msg = 'OO고등학교 출결관리앱 v1.0'


# 메인 윈도우 클래스 정의
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()  # UI 초기화 함수 호출

    # UI 초기화 함수
    def initUI(self):
        # UI 파일 로드
        uic.loadUi('./teamproject/학생 로그인 화면.ui', self)
        self.setWindowTitle('학생용 로그인')  # 윈도우 제목 설정
        self.setWindowIcon(QIcon('./image/app01.png'))

        # 로그인 버튼 클릭 시그널 연결
        self.btn_login.clicked.connect(self.btnLogClick)

        # 상태바에 메시지 추가
        self.statusbar.showMessage(basic_msg)

    # 입력 필드 초기화 함수
    def clearInput(self):
        self.input_S_ID.clear()  # 아이디 입력 필드 초기화
        self.input_S_PW.clear()  # 비밀번호 입력 필드 초기화

    # 로그인 버튼 클릭 이벤트 처리 함수
    def btnLogClick(self):
        # 입력 필드에서 아이디와 비밀번호 값 가져오기
        S_ID = self.input_S_ID.text()
        S_PW = self.input_S_PW.text()

        # 입력값 검증 (Validation Check)
        if S_ID == '' or S_PW == '':
            # 입력값이 비어있을 경우 경고 메시지 표시
            QMessageBox.warning(self, '경고', '학번 또는 비밀번호 입력은 필수입니다!')
            return  # 함수 종료
        else:
            print('로그인 진행!') 
            values = (S_ID, S_PW)  # 입력값을 튜플로 저장
            # 데이터베이스에서 로그인 정보 확인
            if self.addData(values) == True:  # 로그인 성공
                QMessageBox.about(self, '로그인 성공!', '어서오세요!')
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
                      FROM STUDENT
                     WHERE S_ID = :v_S_ID
                       AND S_PW = :v_S_PW
                    '''
            # 쿼리 실행 (바인딩 변수 사용)
            cursor.execute(query, {'v_S_ID': values[0], 'v_S_PW': values[1]})
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

    def btnLogClick(self):
        self.studentlogin_window = StudentloginWindow()
        self.studentlogin_window.show()
        self.close()

class StudentloginWindow(QMainWindow):
    def __init__(self):
        super(StudentloginWindow, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./teamproject/로그인 방식.ui', self)
        self.setWindowTitle('로그인 방식')

        # 프로그램 실행 진입점
if __name__ == '__main__':
    app = QApplication(sys.argv)  # QApplication 객체 생성
    win = MainWindow()  # MainWindow 객체 생성
    win.show()  # 메인 윈도우 표시
    app.exec_()  # 이벤트 루프 실행