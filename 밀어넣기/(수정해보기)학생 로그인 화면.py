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

# 메인 윈도우 클래스 정의
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()  # UI 초기화 함수 호출

    # UI 초기화 함수
    def initUI(self):
        uic.loadUi('./학생 로그인 화면.ui', self)
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
        S_ID = self.input_S_ID.text()
        S_PW = self.input_S_PW.text()

        self.S_ID = self.input_S_ID.text() # 로그인한 ID 변수값에 저장 

        if S_ID == '' or S_PW == '':
            QMessageBox.warning(self, '경고', '학번 또는 비밀번호 입력은 필수입니다!')
            return
        else:
            print('로그인 진행!')
            values = (S_ID, S_PW)
            if self.addData(values) == True:
                QMessageBox.about(self, '로그인 성공!', '어서오세요!')
                self.studentAttendanceWindow()
            else:
                QMessageBox.about(self, '로그인 실패!', '로그인 실패, 관리자에게 문의하세요.')
        self.clearInput()

    # 데이터베이스에서 로그인 정보 확인 함수
    def addData(self, values):
        isSucceed = False
        conn = oci.connect(f'{username}/{password}@{host}:{port}/{sid}')
        cursor = conn.cursor()

        try:
            query = '''
                    SELECT COUNT(*)
                      FROM STUDENT
                     WHERE S_ID = :v_S_ID
                       AND S_PW = :v_S_PW
                    '''
            cursor.execute(query, {'v_S_ID': values[0], 'v_S_PW': values[1]})
            result = cursor.fetchone()


            if result[0] > 0:
                isSucceed = True
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
        finally:
            cursor.close()
            conn.close()

        return isSucceed
    
    def studentAttendanceWindow(self):
        self.studentlogin_window = StudentloginWindow(self.s_ID)
        self.studentlogin_window.show()
        self.close()  # 현재 창을 닫기


class StudentloginWindow(QMainWindow):
    def __init__(self):
        super(StudentloginWindow, self).__init__()
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

        self.atdcheckpage_window = AtdCheckWindow()
        self.atdcheckpage_window.show()


class MypageWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        uic.loadUi('./mypage.ui', self)
        self.setWindowTitle('마이페이지')

        # 테이블 위젯이 UI에 존재하는지 확인
        self.btlstudent = self.findChild(QTableWidget, "btlstudent")
        if self.btlstudent is None:
            QMessageBox.critical(self, "오류", "QTableWidget(btlstudent)이 UI에 없습니다.")
            return

        # 버튼 이벤트 연결
        self.btn_upload.clicked.connect(self.uploadPhoto)
        self.btn_search.clicked.connect(self.btnSearchClick)
        self.btn_insert.clicked.connect(self.btnInsertClick)
        self.btn_update.clicked.connect(self.updateStudentInfo)
        self.btn_delete.clicked.connect(self.btnDeleteClick)
        self.btn_show_all.clicked.connect(self.loadData)
        self.btlstudent.cellDoubleClicked.connect(self.showStudentDetails)
        

        # 데이터 불러오기
        self.loadData()
        
    def uploadPhoto(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "사진 업로드", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)", options=options)

        if file_path:
            pixmap = QPixmap(file_path)
            resized_pixmap = pixmap.scaled(300, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation) 
            self.photo_label.setPixmap(resized_pixmap)  # QLabel에 표시
            self.photo_path = file_path

    def loadData(self):
        try:
            connection = oci.connect(username, password, f"{host}:{port}/{sid}")
            cursor = connection.cursor()
            
            query = """SELECT s_name, s_id, s_pw, 
                          TO_CHAR(s_birth, 'YYYY-MM-DD') AS s_birth, 
                          s_tel, s_addr, class_no, s_no 
                   FROM student
                   ORDER BY CASE WHEN s_no = 1 THEN 0 ELSE 1 END, s_no"""
            cursor.execute(query)
            data = cursor.fetchall()
            
            # 테이블 초기화
            self.btlstudent.clearContents()
            self.btlstudent.setRowCount(len(data))
            self.btlstudent.setColumnCount(len(data[0]) if data else 8)
            self.btlstudent.setHorizontalHeaderLabels(["이름", "ID", "PWD", "생년월일", "전화번호", "주소", "반", "번호"])

            for row_idx, row_data in enumerate(data):
                for col_idx, col_data in enumerate(row_data):
                    self.btlstudent.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        except oci.DatabaseError as e:
            QMessageBox.critical(self, "데이터베이스 오류", f"오류 내용: {str(e)}")
        finally:
            cursor.close()
            connection.close()

    def btnSearchClick(self):
        """입력된 이름으로 학생 검색"""
        std_name = self.input_std_name.text().strip()
        if not std_name:
            QMessageBox.warning(self, "검색 오류", "검색할 이름을 입력하세요.")
            return
        
        try:
            connection = oci.connect(username, password, f"{host}:{port}/{sid}")
            cursor = connection.cursor()

            query = """SELECT s_name, s_id, s_pw, TO_CHAR(s_birth, 'YYYY-MM-DD') AS s_birth, 
                              s_tel, s_addr, class_no, s_no 
                       FROM student
                       WHERE s_name LIKE :s_name"""
            cursor.execute(query, {"s_name": f"%{std_name}%"})
            data = cursor.fetchall()

            if not data:
                QMessageBox.information(self, "검색 결과", "해당 이름을 가진 학생이 없습니다.")
                return
            
            self.loadTableData(data)

        except oci.DatabaseError as e:
            QMessageBox.critical(self, "DB 오류", f"오류 내용: {str(e)}")

        finally:
            cursor.close()
            connection.close()

    def loadTableData(self, data):
        """QTableWidget에 검색된 데이터 로드"""
        self.btlstudent.setRowCount(len(data))
        self.btlstudent.setColumnCount(8)
        self.btlstudent.setHorizontalHeaderLabels(
            ["이름", "ID", "PWD", "생년월일", "전화번호", "주소", "반", "번호"]
        )

        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                self.btlstudent.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

    def btnInsertClick(self):
        """학생 정보 추가"""
        name = self.std_name.text().strip()
        std_id = self.std_id.text().strip()
        pwd = self.std_pwd.text().strip()
        birth = f"{self.cmb_year.currentText()}-{self.cmb_month.currentText()}-{self.cmb_day.currentText()}"
        tel = self.std_tel.text().strip()
        addr = self.std_addr.text().strip()
        class_no = self.cmb_class.currentText()
        s_no = self.std_number.text().strip()

        if not (name and std_id and pwd and tel and addr and class_no and s_no):
            QMessageBox.warning(self, "입력 오류", "모든 필드를 입력하세요.")
            return

        try:
            connection = oci.connect(username, password, f"{host}:{port}/{sid}")
            cursor = connection.cursor()

            query = """INSERT INTO student (s_name, s_id, s_pw, s_birth, s_tel, s_addr, class_no, s_no)
                       VALUES (:name, :std_id, :pwd, TO_DATE(:birth, 'YYYY-MM-DD'), :tel, :addr, :class_no, :s_no)"""

            cursor.execute(query, {
                "name": name, "std_id": std_id, "pwd": pwd, "birth": birth,
                "tel": tel, "addr": addr, "class_no": class_no, "s_no": s_no
            })
            connection.commit()
            QMessageBox.information(self, "입력 성공", "학생 정보가 추가되었습니다.")
            self.loadData()  # 데이터 새로고침

        except oci.DatabaseError as e:
            QMessageBox.critical(self, "DB 오류", f"오류 내용: {str(e)}")

        finally:
            cursor.close()
            connection.close()

    def updateStudentInfo(self):
        """학생 정보 수정"""
        std_id = self.std_id.text().strip()  # ID (변경 불가)
        name = self.std_name.text().strip()
        pwd = self.std_pwd.text().strip()
        birth = f"{self.cmb_year.currentText()}-{self.cmb_month.currentText()}-{self.cmb_day.currentText()}"
        tel = self.std_tel.text().strip()
        addr = self.std_addr.text().strip()
        class_no = self.cmb_class.currentText()
        s_no = self.std_number.text().strip()

        if not (name and pwd and tel and addr and class_no and s_no):
            QMessageBox.warning(self, "입력 오류", "모든 필드를 입력하세요.")
            return

        try:
            connection = oci.connect(username, password, f"{host}:{port}/{sid}")
            cursor = connection.cursor()

            query = """UPDATE student 
                    SET s_name = :name, s_pw = :pwd, s_birth = TO_DATE(:birth, 'YYYY-MM-DD'), 
                        s_tel = :tel, s_addr = :addr, class_no = :class_no, s_no = :s_no
                    WHERE s_id = :std_id"""
            cursor.execute(query, {
                "name": name, "pwd": pwd, "birth": birth, "tel": tel, 
                "addr": addr, "class_no": class_no, "s_no": s_no, "std_id": std_id
            })
            connection.commit()

            QMessageBox.information(self, "수정 성공", "학생 정보가 수정되었습니다.")
            self.loadData()  # 테이블 새로고침

        except oci.DatabaseError as e:
            QMessageBox.critical(self, "DB 오류", f"오류 내용: {str(e)}")

        finally:
            cursor.close()
            connection.close()

    def btnDeleteClick(self):
        """학생 정보 삭제"""
        selected_row = self.btlstudent.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "삭제 오류", "삭제할 학생을 선택하세요.")
            return

        std_id = self.btlstudent.item(selected_row, 1).text()

        try:
            connection = oci.connect(username, password, f"{host}:{port}/{sid}")
            cursor = connection.cursor()

            query = "DELETE FROM student WHERE s_id = :std_id"
            cursor.execute(query, {"std_id": std_id})
            connection.commit()
            QMessageBox.information(self, "삭제 성공", "학생 정보가 삭제되었습니다.")
            self.loadData()

        except oci.DatabaseError as e:
            QMessageBox.critical(self, "DB 오류", f"오류 내용: {str(e)}")

        finally:
            cursor.close()
            connection.close()

    def showStudentDetails(self, row):
        """학생 이름을 더블클릭하면 정보 로드"""
        std_id = self.btlstudent.item(row, 1).text()  # 학생 ID 가져오기
        
        try:
            connection = oci.connect(username, password, f"{host}:{port}/{sid}")
            cursor = connection.cursor()

            query = """SELECT s_name, s_id, s_pw, 
                            TO_CHAR(s_birth, 'YYYY-MM-DD') AS s_birth, 
                            s_tel, s_addr, class_no, s_no 
                    FROM student
                    WHERE s_id = :std_id"""
            cursor.execute(query, {"std_id": std_id})
            student_data = cursor.fetchone()

            if student_data:
            # UI 필드에 데이터 채우기
                self.std_name.setText(student_data[0])  # 이름
                self.std_id.setText(student_data[1]) # id
                self.std_id.setDisabled(False) 
                self.std_pwd.setText(student_data[2])  # 비밀번호
                birth_date = student_data[3].split('-')
                self.cmb_year.setCurrentText(birth_date[0])  # 년도
                self.cmb_month.setCurrentText(birth_date[1])  # 월
                self.cmb_day.setCurrentText(birth_date[2])  # 일
                self.std_tel.setText(student_data[4])  # 전화번호
                self.std_addr.setText(student_data[5])  # 주소
                self.cmb_class.setCurrentText(str(student_data[6]))  # 반
                self.std_number.setText(str(student_data[7]))  # 번호

                # 수정 버튼 활성화
                self.btn_update.setEnabled(True)

            else:
             QMessageBox.warning(self, "조회 오류", "학생 정보를 찾을 수 없습니다.")

        except oci.DatabaseError as e:
            QMessageBox.critical(self, "DB 오류", f"오류 내용: {str(e)}")

        finally:
            cursor.close()
            connection.close()
      

class AtdCheckWindow(QMainWindow): 
    def __init__(self):
        super(AtdCheckWindow, self).__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('./출석관리,통계.ui', self)
        self.setWindowTitle('출석관리')
        self.setWindowIcon(QIcon('./image/app01.png'))

# 프로그램 실행 진입점
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exec_()