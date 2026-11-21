import sqlite3, random

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE 출장 (출장번호 INTEGER PRIMARY KEY, 직원번호 INTEGER,"
           " 출발일 TEXT, 목적지 TEXT)")
random.seed(42)                                  # 매번 같은 연습 데이터를 만든다
cities = ["부산", "대구", "광주", "대전", "울산", "제주"]
db.executemany("INSERT INTO 출장 VALUES (?, ?, ?, ?)",
               [(i, random.randint(1000, 5999),
                 f"2026-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                 random.choice(cities)) for i in range(1, 200_001)])

sql = "SELECT 출발일, 목적지 FROM 출장 WHERE 직원번호 = 1001"
def plan():
    return db.execute("EXPLAIN QUERY PLAN " + sql).fetchone()[-1]

print("출장 기록:", db.execute("SELECT COUNT(*) FROM 출장").fetchone()[0], "건")
print("인덱스 전 계획:", plan())
db.execute("CREATE INDEX 출장_직원번호 ON 출장(직원번호)")
print("인덱스 후 계획:", plan())
print("1001번 직원의 출장:", len(db.execute(sql).fetchall()), "건")
