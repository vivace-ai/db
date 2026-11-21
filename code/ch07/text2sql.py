import sqlite3, pathlib, re

# 준비: 연습용 데이터베이스 파일을 만들고, 쓰기 연결은 바로 닫는다
DB = pathlib.Path(__file__).with_name("agentdb.sqlite")
DB.unlink(missing_ok=True)
w = sqlite3.connect(DB)
w.executescript("""
CREATE TABLE 부서 (부서번호 INTEGER PRIMARY KEY, 부서명 TEXT NOT NULL);
CREATE TABLE 직원 (직원번호 INTEGER PRIMARY KEY, 이름 TEXT NOT NULL, 직급 TEXT,
                   부서번호 INTEGER REFERENCES 부서);
CREATE TABLE 임원보수 (이름 TEXT, 연봉 INTEGER);          -- 에이전트가 보면 안 되는 표
INSERT INTO 부서 VALUES (10, '영업팀'), (20, '재무팀'), (30, '인사팀');
INSERT INTO 직원 VALUES (1001, '민지', '대리', 10), (1002, '준호', '과장', 20),
    (1003, '서연', '사원', 10), (1004, '도윤', '부장', 30), (1005, '민지', '사원', 20);
INSERT INTO 임원보수 VALUES ('사장', 999);
""")
w.close()

ALLOWED = {"부서", "직원"}                                    # 볼 수 있는 표 목록

# [겹4] 데이터베이스 권한: 읽기 전용 연결 + 권한 검사기
ro = sqlite3.connect(DB.as_uri() + "?mode=ro", uri=True)
def guard(action, name, *_):
    if action in (sqlite3.SQLITE_SELECT, sqlite3.SQLITE_FUNCTION):
        return sqlite3.SQLITE_OK
    if action == sqlite3.SQLITE_READ and name in ALLOWED:  # 허용한 표만 읽기
        return sqlite3.SQLITE_OK
    return sqlite3.SQLITE_DENY                              # 쓰기·ATTACH·PRAGMA 등은 모두 거절
ro.set_authorizer(guard)

def check(sql):                                          # [겹1·2] 실행 전 코드 검사
    s = sql.strip().rstrip(";")
    if ";" in s:
        return "문장은 하나만"
    if not re.match(r"(?i)select\b", s):
        return "SELECT만 허용"
    tables = set(re.findall(r"(?i)\b(?:from|join)\s+(\w+)", s))
    if not tables <= ALLOWED:
        return f"허용되지 않은 표 {sorted(tables - ALLOWED)}"
    return None

def run(sql, limit=20):                                  # [겹3] 줄 수 제한을 씌워 실행
    problem = check(sql)
    if problem:
        return False, f"막음: {problem}"
    try:
        s = sql.strip().rstrip(";")
        return True, ro.execute(f"SELECT * FROM ({s}\n) LIMIT {limit}").fetchall()
    except sqlite3.DatabaseError as e:
        if "prohibited" in str(e) or "not authorized" in str(e):
            return False, f"막음(데이터베이스): {e}"
        return False, f"오류: {e}"

def fake_llm(question, error=None):    # 진짜 LLM 대신 정해 둔 SQL을 돌려주는 흉내
    tries = {
        "영업팀은 몇 명이에요?": [
            "SELECT COUNT(*) FROM 직원 WHERE 팀 = '영업팀'",
            "SELECT COUNT(*) FROM 직원 JOIN 부서 USING (부서번호) WHERE 부서명 = '영업팀'"],
        "준호 님을 퇴사 처리해 줘": ["DELETE FROM 직원 WHERE 이름 = '준호'"],
        "사장님 연봉이 얼마예요?": ['SELECT 연봉 FROM "임원보수"'],
    }[question]
    return tries[1] if error and len(tries) > 1 else tries[0]

def agent(question):                       # 오류가 나면 알려 주고 한 번 더, 막히면 멈춤
    error = None
    for attempt in (1, 2):
        sql = fake_llm(question, error)
        ok, result = run(sql)
        print(f"  {attempt}차 SQL: {sql}")
        print(f"     {'✓' if ok else '✕'} {result}")
        if ok or result.startswith("막음"):
            return
        error = result

for q in ["영업팀은 몇 명이에요?", "준호 님을 퇴사 처리해 줘", "사장님 연봉이 얼마예요?"]:
    print("질문:", q)
    agent(q)

print("검사를 거치지 않고 데이터베이스에 직접 보내면:")
for sql in ["UPDATE 직원 SET 직급 = '부장'", f"ATTACH '{DB.as_uri()}' AS w"]:
    try:
        ro.execute(sql)
    except sqlite3.DatabaseError as e:
        print(f"  ✕ {sql.split()[0]}: {e}")
