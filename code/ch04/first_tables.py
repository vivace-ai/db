import sqlite3

db = sqlite3.connect(":memory:")
db.execute("PRAGMA foreign_keys = ON")   # 외래 키 검사 켜기 (SQLite는 기본이 꺼져 있음)
db.executescript("""
CREATE TABLE 부서 (
    부서번호 INTEGER PRIMARY KEY,
    부서명   TEXT    NOT NULL UNIQUE
);
CREATE TABLE 직원 (
    직원번호 INTEGER PRIMARY KEY,
    이름     TEXT    NOT NULL,
    직급     TEXT    NOT NULL CHECK (직급 IN ('사원', '대리', '과장', '부장')),
    부서번호 INTEGER NOT NULL REFERENCES 부서(부서번호)
);
""")
db.executemany("INSERT INTO 부서 VALUES (?, ?)", [(10, "영업팀"), (20, "재무팀")])
db.executemany("INSERT INTO 직원 VALUES (?, ?, ?, ?)",
               [(1001, "민지", "대리", 10), (1002, "준호", "과장", 20),
                (1005, "민지", "사원", 20)])

tests = [("직원번호 중복", (1001, "지수", "사원", 10)),
         ("없는 직급",     (1006, "지수", "인턴", 10)),
         ("없는 부서",     (1007, "지수", "사원", 99)),
         ("올바른 값",     (1008, "지수", "사원", 10))]
for name, row in tests:
    try:
        db.execute("INSERT INTO 직원 VALUES (?, ?, ?, ?)", row)
        print(f"✓ {name}: 들어감")
    except sqlite3.IntegrityError as e:
        print(f"✕ {name}: 거절 ({e})")

print()
rows = db.execute("SELECT 직원번호, 이름, 직급, 부서명 FROM 직원 "
                  "JOIN 부서 USING (부서번호) ORDER BY 직원번호")
for row in rows:
    print(row)
