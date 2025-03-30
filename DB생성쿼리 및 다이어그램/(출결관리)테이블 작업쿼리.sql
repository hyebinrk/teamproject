SELECT  * FROM student;

ALTER TABLE atd
ADD (
    leave_time TIMESTAMP DEFAULT SYSTIMESTAMP,         -- 조퇴 시간 (기본값: 현재 시간)
    out_time  TIMESTAMP DEFAULT SYSTIMESTAMP,          -- 외출 시간 (기본값: 현재 시간)
    in_time   TIMESTAMP DEFAULT SYSTIMESTAMP           -- 복귀 시간 (기본값: 현재 시간)
);



--class
SELECT * FROM CLASS;

INSERT INTO CLASS
	VALUES(CLASS_CLASS_NO_SEQ.nextval, '01', TEACHER_T_NO_SEQ.nextval);

--student
SELECT * FROM student;

SELECT s_no, s_id, s_pw, s_name, s_birth, s_tel, s_addr, class_no
	FROM student
	WHERE s_id = 1;

INSERT INTO STUDENT
	VALUES(STUDENT_S_NO_SEQ.nextval, '1', '12345', '학생', '2007-11-18', '010-0221-0221', '서울시 왕십리로 83-21', '01');

--teacher
SELECT * FROM teacher;

INSERT INTO teacher
	VALUES(teacher_t_NO_SEQ.nextval, '1', '12345', '교사', '010-1111-1111', '01');

--atd
SELECT * FROM atd;

INSERT INTO atd(atd_no, s_no, t_no)
	values('1', '3', '2');

INSERT INTO atd(atd_no, s_no, t_no)
	values('2', '8', '2');

INSERT INTO atd(atd_no, s_no, t_no)
	values('3', '11', '2');

UPDATE ATD
	SET atd_date = systimestamp
	WHERE s_no = 3;

--우리나라 시간으로
UPDATE ATD
SET atd_date = CAST(SYSTIMESTAMP AT TIME ZONE 'UTC' AS TIMESTAMP WITH TIME ZONE) AT TIME ZONE 'Asia/Seoul'
WHERE s_no = 3;

	
--조퇴 버튼 눌렀을 때 적용시킬 쿼리
UPDATE atd
	SET leave_time = SYSTIMESTAMP
	WHERE s_no = 3
		AND trunc(atd_date) = trunc(sysdate) ; --변수1 값에 아이디 저장시키고 그에 해당하는 s_no을 찾아내 저장시킨 변수2가 s_id

ROLLBACK;


--외출 버튼 눌렀을 때 적용시킬 쿼리
UPDATE atd
	SET out_time = SYSTIMESTAMP
	WHERE s_no = 3
		AND trunc(atd_date) = trunc(sysdate) ; --변수1 값에 아이디 저장시키고 그에 해당하는 s_no을 찾아내 저장시킨 변수2가 s_id
		
ROLLBACK;
		
--복귀 버튼 눌렀을 때 적용시킬 쿼리
UPDATE atd
	SET in_time = SYSTIMESTAMP
		WHERE s_no = 3
			AND trunc(out_time) = trunc(sysdate) ; --변수1 값에 아이디 저장시키고 그에 해당하는 s_no을 찾아내 저장시킨 변수2가 s_id
			

COMMIT;




INSERT INTO ATTENDANCE.ATD
(ATD_NO, S_NO, ATD_DATE, ATD_TIME)
VALUES(atd_no_seq.nextval, student_s_no_seq.nextval, SYSDATE, SYSTIMESTAMP);
