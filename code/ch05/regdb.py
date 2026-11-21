import sqlite3, pathlib

DB = pathlib.Path(__file__).with_name("regdb.sqlite")   # 이 프로그램과 같은 폴더에
DB.unlink(missing_ok=True)          # 연습할 때마다 깨끗한 상태에서 새로 만든다
db = sqlite3.connect(DB)
db.executescript("""
PRAGMA foreign_keys = ON;
CREATE TABLE 부서 (부서번호 INTEGER PRIMARY KEY, 부서명 TEXT NOT NULL UNIQUE);
CREATE TABLE 직원 (직원번호 INTEGER PRIMARY KEY, 이름 TEXT NOT NULL,
                   직급 TEXT NOT NULL, 부서번호 INTEGER NOT NULL REFERENCES 부서);
CREATE TABLE 규정 (규정번호 INTEGER PRIMARY KEY, 규정명 TEXT NOT NULL,
                   담당부서번호 INTEGER NOT NULL REFERENCES 부서);
CREATE TABLE 규정조항 (조항번호 INTEGER PRIMARY KEY,
                       규정번호 INTEGER NOT NULL REFERENCES 규정,
                       항목 TEXT NOT NULL, 값 TEXT NOT NULL,
                       시행일 TEXT NOT NULL, 종료일 TEXT);
CREATE TABLE 규정적용 (규정번호 INTEGER REFERENCES 규정,
                       부서번호 INTEGER REFERENCES 부서,
                       PRIMARY KEY (규정번호, 부서번호));

INSERT INTO 부서 VALUES (10, '영업팀'), (20, '재무팀'), (30, '인사팀'), (40, '보안팀');
INSERT INTO 직원 VALUES (1001, '민지', '대리', 10), (1002, '준호', '과장', 20),
    (1003, '서연', '사원', 10), (1004, '도윤', '부장', 30), (1005, '민지', '사원', 20);
INSERT INTO 규정 VALUES (1, '국내 출장 규정', 20), (2, '법인카드 규정', 20),
    (3, '취업 규칙', 30);
INSERT INTO 규정조항 VALUES
    (1, 1, '식비 한도', '하루 3만 원', '2025-01-01', '2026-10-31'),
    (2, 1, '식비 한도', '하루 4만 원', '2026-11-01', NULL),
    (3, 1, '숙박비 한도', '하루 7만 원', '2025-01-01', NULL),
    (4, 3, '연차 기본 일수', '15일', '2025-01-01', NULL);
INSERT INTO 규정적용 VALUES (1, 10), (1, 20), (2, 10), (2, 20), (3, 10), (3, 20), (3, 30);
""")
db.commit()
for t in ["부서", "직원", "규정", "규정조항", "규정적용"]:
    print(f"{t}: {db.execute(f'SELECT COUNT(*) FROM {t}').fetchone()[0]}줄")
