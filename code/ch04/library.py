import sqlite3

db = sqlite3.connect(":memory:")
db.execute("PRAGMA foreign_keys = ON")
db.executescript("""
CREATE TABLE 회원 (회원번호 INTEGER PRIMARY KEY, 이름 TEXT NOT NULL);
CREATE TABLE 책   (책번호   INTEGER PRIMARY KEY, 제목 TEXT NOT NULL);
CREATE TABLE 대출 (                                  -- 회원과 책을 잇는 연결 표
    대출번호 INTEGER PRIMARY KEY,
    회원번호 INTEGER NOT NULL REFERENCES 회원(회원번호),
    책번호   INTEGER NOT NULL REFERENCES 책(책번호),
    대출일   TEXT    NOT NULL,
    반납일   TEXT    CHECK (반납일 IS NULL OR 반납일 >= 대출일)   -- 비어 있으면 대출 중
);
CREATE UNIQUE INDEX 한권은한사람만 ON 대출(책번호) WHERE 반납일 IS NULL;
""")
db.executemany("INSERT INTO 회원 VALUES (?, ?)", [(1, "하늘"), (2, "바다")])
db.executemany("INSERT INTO 책 VALUES (?, ?)",
               [(101, "별의 지도"), (102, "숲의 시간"), (103, "바람 일기")])
db.executemany("INSERT INTO 대출 VALUES (?, ?, ?, ?, ?)",
               [(1, 1, 101, "2026-11-01", "2026-11-10"),     # 하늘이 빌렸다가 반납
                (2, 2, 101, "2026-11-12", None),             # 같은 책을 바다가 빌려 감
                (3, 1, 102, "2026-11-12", None)])            # 하늘은 다른 책도 빌림

tests = [("빌려 간 책을 또 빌리기",   (4, 1, 101, "2026-11-13", None)),
         ("반납일이 대출일보다 앞",   (5, 2, 103, "2026-11-13", "2026-11-01")),
         ("없는 회원",               (6, 9, 103, "2026-11-13", None)),
         ("올바른 대출",             (7, 2, 103, "2026-11-13", None))]
for name, row in tests:
    try:
        db.execute("INSERT INTO 대출 VALUES (?, ?, ?, ?, ?)", row)
        print(f"✓ {name}: 들어감")
    except sqlite3.IntegrityError as e:
        print(f"✕ {name}: 거절 ({e})")

print()
for row in db.execute("SELECT 이름, 제목, 대출일, IFNULL(반납일, '대출 중') FROM 대출 "
                      "JOIN 회원 USING (회원번호) JOIN 책 USING (책번호) ORDER BY 대출번호"):
    print(row)
