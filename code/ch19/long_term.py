import re, sqlite3

db = sqlite3.connect(":memory:")
db.execute("""CREATE TABLE 기억 (직원번호 INTEGER, 항목 TEXT, 값 TEXT, 출처 TEXT,
              갱신 TEXT, PRIMARY KEY (직원번호, 항목))""")
db.execute("""CREATE TABLE 기억이력 (직원번호 INTEGER, 항목 TEXT, 옛값 TEXT,
              바뀐날 TEXT)""")

SENSITIVE = re.compile(r"\d{6}-\d{7}|병원|진단|약을")    # 남기지 않을 정보

def remember(emp, item, value, src, now):
    if SENSITIVE.search(value):
        return f"✕ 거름   {item}: 민감한 정보라 남기지 않는다"
    old = db.execute("SELECT 값 FROM 기억 WHERE 직원번호 = ? AND 항목 = ?",
                     (emp, item)).fetchone()
    with db:                                             # 이력과 새 값을 함께
        if old:
            db.execute("INSERT INTO 기억이력 VALUES (?, ?, ?, ?)",
                       (emp, item, old[0], now))
        db.execute("""INSERT INTO 기억 VALUES (?, ?, ?, ?, ?)
                      ON CONFLICT (직원번호, 항목) DO UPDATE
                      SET 값 = excluded.값, 출처 = excluded.출처,
                          갱신 = excluded.갱신""",
                   (emp, item, value, src, now))
    if old:
        return f"↻ 바꿈   {item}: {old[0]} → {value}"
    return f"✓ 새로   {item}: {value}"

def recall(emp):                                         # 주인의 기억만 꺼낸다
    return db.execute("SELECT 항목, 값, 출처 FROM 기억 WHERE 직원번호 = ? "
                      "ORDER BY 항목", (emp,)).fetchall()

# 11월 13일 대화(s-0007)가 끝난 뒤, LLM이 골라 준 기억 후보의 예
for item, value in [("답 형식", "표로 정리"), ("자주 가는 출장지", "부산"),
                    ("건강", "허리 때문에 병원에 다닌다"),
                    ("본인 확인", "900101-2345678")]:
    print(remember(1001, item, value, "s-0007", "2026-11-13"))
# 11월 20일 대화(s-0012): "이제 표 말고 짧게 두세 줄로 주세요"
print(remember(1001, "답 형식", "짧은 문장 두세 줄", "s-0012", "2026-11-20"))

print("민지(1001)의 장기 기억")
for row in recall(1001):
    print("  ", row)
print("바뀐 이력:", db.execute("SELECT 항목, 옛값, 바뀐날 FROM 기억이력").fetchall())
print("서연(1003)의 장기 기억:", recall(1003))
