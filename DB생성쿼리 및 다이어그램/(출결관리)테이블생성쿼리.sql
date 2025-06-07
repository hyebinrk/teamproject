CREATE TABLE class (
    class_no   NUMBER PRIMARY KEY,      -- 반 ID (기본키)
    class_name VARCHAR2(50) NOT NULL,   -- 반 이름
    t_no       NUMBER                   -- 담당 교사 ID (외래키, teacher 테이블 참조)
);

CREATE TABLE teacher (
    t_no     NUMBER PRIMARY KEY,           -- 교사 고유 번호
    t_id     VARCHAR2(50) UNIQUE NOT NULL, -- 로그인 아이디
    t_pw     VARCHAR2(255) NOT NULL,       -- 비밀번호 (암호화 권장)
    t_name   VARCHAR2(50) NOT NULL,        -- 이름
    t_tel    VARCHAR2(20),                 -- 전화번호
    class_no NUMBER,                       -- 담당 반 ID (외래키)
    CONSTRAINT fk_teacher_class FOREIGN KEY (class_no) REFERENCES class(class_no) 
);

CREATE TABLE student (
    s_no    NUMBER PRIMARY KEY,            -- 학생 고유 번호
    s_id     VARCHAR2(50) UNIQUE NOT NULL, -- 로그인 아이디
    s_pw     VARCHAR2(255) NOT NULL,       -- 비밀번호 (암호화 권장)
    s_name   VARCHAR2(50) NOT NULL,        -- 이름
    s_birth  DATE NOT NULL,                 -- 생년월일
    s_tel    VARCHAR2(20),                 -- 전화번호
    s_addr   VARCHAR2(255),                  -- 주소
    class_no NUMBER,                       -- 반 ID (외래키)
--    checkno  VARCHAR2(10),                 -- 출석번호 (교사가 생성한 번호) 
    CONSTRAINT fk_student_class FOREIGN KEY (class_no) REFERENCES class(class_no)
);

CREATE TABLE atd (
    atd_no   NUMBER    PRIMARY KEY,                     -- 출결 ID (기본키)
    s_no     NUMBER    NOT NULL,                       -- 학생 ID (외래키)
    atd_date DATE      DEFAULT SYSDATE,                 -- 출석 날짜 (기본값: 오늘 날짜)
    atd_time TIMESTAMP DEFAULT SYSTIMESTAMP,             -- 출석 시간 (기본값: 현재 시간)
    status     CHAR(1)   CHECK (status IN ('P', 'A', 'L')), -- 출석 상태 ('P': 출석, 'A': 결석, 'L': 지각)
    t_no    NUMBER,                                   -- 담당 교사 ID (외래키)
    checkno  VARCHAR2(10),                                -- 출석번호 (교사가 생성한 번호와 비교)
    CONSTRAINT fk_atd_student FOREIGN KEY (s_no) REFERENCES student(s_no),
    CONSTRAINT fk_atd_teacher FOREIGN KEY (t_no) REFERENCES teacher(t_no)
);

-- 테이블 수정(컬럼 추가)
ALTER TABLE atd
ADD (
    leave_time TIMESTAMP DEFAULT SYSTIMESTAMP,         -- 조퇴 시간 (기본값: 현재 시간)
    out_time  TIMESTAMP DEFAULT SYSTIMESTAMP,          -- 외출 시간 (기본값: 현재 시간)
    in_time   TIMESTAMP DEFAULT SYSTIMESTAMP           -- 복귀 시간 (기본값: 현재 시간)
);


-- 새로 추가된 테이블
CREATE TABLE check_attendance (
    check_id   NUMBER PRIMARY KEY,      -- 출석 인증 ID
    class_no   NUMBER NOT NULL,         -- 반 ID (외래키)
    checkno    VARCHAR2(10) NOT NULL,   -- 출석번호
    t_no       NUMBER NOT NULL,         -- 출석번호 생성한 교사 ID (외래키)
    CONSTRAINT fk_check_class FOREIGN KEY (class_no) REFERENCES class(class_no),
    CONSTRAINT fk_check_teacher FOREIGN KEY (t_no) REFERENCES teacher(t_no)
);



CREATE OR REPLACE TRIGGER set_atd_status
BEFORE INSERT ON atd
FOR EACH ROW
BEGIN
    IF :NEW.status IS NULL THEN
        IF TO_CHAR(SYSTIMESTAMP, 'HH24:MI:SS') <= '08:59:59' THEN
            :NEW.status := 'P'; -- 출석
        ELSIF TO_CHAR(SYSTIMESTAMP, 'HH24:MI:SS') BETWEEN '09:00:00' AND '12:59:59' THEN
            :NEW.status := 'L'; -- 지각
        ELSE
            :NEW.status := 'A'; -- 결석
        END IF;
    END IF;
END;


CREATE SEQUENCE atd_no_seq
START WITH 1
INCREMENT BY 1;

CREATE SEQUENCE student_s_no_seq
START WITH 1
INCREMENT BY 1;

CREATE SEQUENCE teacher_t_no_seq
START WITH 1
INCREMENT BY 1;

CREATE SEQUENCE class_class_no_seq
START WITH 1
INCREMENT BY 1;

CREATE SEQUENCE check_attendance_check_id_seq
START WITH 1
INCREMENT BY 1;

COMMIT;