import sqlite3, json, pathlib

DB = pathlib.Path(__file__).with_name("chatdb.sqlite")
DB.unlink(missing_ok=True)
db = sqlite3.connect(DB)
db.execute("""CREATE TABLE 대화 (
    세션ID TEXT PRIMARY KEY,
    문서   TEXT NOT NULL CHECK (json_valid(문서)))""")      # 올바른 JSON만 받는다

def j(value):
    return json.dumps(value, ensure_ascii=False)

def new_session(sid, emp, now):                         # 대화 한 건 = 문서 한 개
    doc = {"세션ID": sid, "직원번호": emp, "시작": now, "메시지": []}
    with db:
        db.execute("INSERT INTO 대화 VALUES (?, ?)", (sid, j(doc)))

def add(sid, role, text, now, basis=None):              # 메시지 배열 끝에 덧붙이기
    msg = {"role": role, "content": text, "시각": now}
    if basis:
        msg["근거"] = basis                              # 필요한 메시지에만 붙는 칸
    with db:
        db.execute("UPDATE 대화 SET 문서 = json_insert(문서, '$.메시지[#]', json(?)) "
                   "WHERE 세션ID = ?", (j(msg), sid))

def recent(sid, emp, n):                                # 작업대에 올릴 최근 n개
    rows = db.execute(
        "SELECT json_extract(m.value, '$.role'), json_extract(m.value, '$.content') "
        "FROM 대화, json_each(대화.문서, '$.메시지') AS m "
        "WHERE 세션ID = ? AND json_extract(대화.문서, '$.직원번호') = ? "   # 주인만
        "ORDER BY m.key DESC LIMIT ?", (sid, emp, n)).fetchall()
    return rows[::-1]

def last_basis(emp):                                    # "아까 그 규정"을 찾는다
    return db.execute(
        "SELECT json_extract(m.value, '$.근거.규정'), json_extract(m.value, '$.근거.조항번호'), "
        "json_extract(m.value, '$.content') "
        "FROM 대화, json_each(대화.문서, '$.메시지') AS m "
        "WHERE json_extract(대화.문서, '$.직원번호') = ? "
        "AND json_extract(m.value, '$.근거') IS NOT NULL "
        "ORDER BY json_extract(m.value, '$.시각') DESC LIMIT 1", (emp,)).fetchone()

new_session("s-0001", 1001, "2026-11-20 09:00")
add("s-0001", "user", "다음 주 부산 출장 가요.", "2026-11-20 09:00")
add("s-0001", "assistant", "국내 출장이시군요. 무엇이 궁금하세요?", "2026-11-20 09:00")
add("s-0001", "user", "식비 한도가 얼마예요?", "2026-11-20 09:01")
add("s-0001", "assistant", "하루 4만 원입니다.", "2026-11-20 09:01",
    {"규정": "국내 출장 규정", "조항번호": 2})
add("s-0001", "user", "숙박비는요?", "2026-11-20 09:02")
add("s-0001", "assistant", "하루 7만 원입니다.", "2026-11-20 09:02",
    {"규정": "국내 출장 규정", "조항번호": 3})
new_session("s-0002", 1005, "2026-11-20 09:05")
add("s-0002", "assistant", "1년 근무 시 15일입니다.", "2026-11-20 09:05",
    {"규정": "취업 규칙", "조항번호": 4})

count, with_basis = db.execute(
    "SELECT COUNT(*), COUNT(json_extract(m.value, '$.근거')) "
    "FROM 대화, json_each(대화.문서, '$.메시지') AS m WHERE 세션ID = 's-0001'").fetchone()
print(f"s-0001 · 직원 1001 · 메시지 {count}개 (근거 붙은 답 {with_basis}개)")
print("작업대에 올릴 최근 대화:")
for role, text in recent("s-0001", 1001, 2):
    print(f"  {role}: {text}")
rule, no, said = last_basis(1001)
print(f"직원 1001 “아까 그 규정” → {rule} 조항 {no} ({said})")
rule, no, said = last_basis(1005)
print(f"직원 1005 “아까 그 규정” → {rule} 조항 {no} ({said})")
try:
    with db:
        db.execute("INSERT INTO 대화 VALUES ('s-9999', '{\"메시지\": [')")
except sqlite3.IntegrityError as e:
    print("깨진 JSON 넣기:", e)
