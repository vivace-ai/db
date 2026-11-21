import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE 부서 (부서번호 INTEGER PRIMARY KEY, 부서명 TEXT NOT NULL);
CREATE TABLE 직원 (직원번호 INTEGER PRIMARY KEY, 이름 TEXT NOT NULL, 직급 TEXT,
                   부서번호 INTEGER REFERENCES 부서);
CREATE TABLE 규정조항 (조항번호 INTEGER PRIMARY KEY, 항목 TEXT, 값 TEXT,
                       시행일 TEXT, 종료일 TEXT);
""")
NOTES = {"직원.직급": "사원·대리·과장·부장 중 하나",       # 열마다 붙이는 짧은 설명
         "규정조항.항목": "예: '식비 한도', '숙박비 한도'",
         "규정조항.시행일": "YYYY-MM-DD, 이날부터 유효",
         "규정조항.종료일": "YYYY-MM-DD, 비어 있으면 아직 유효"}

def primary_key(table):
    return next(r[1] for r in db.execute(f"PRAGMA table_info({table})") if r[5])

def schema_text():
    out = []
    for (table,) in db.execute("SELECT name FROM sqlite_master WHERE type = 'table'"):
        fks = {r[3]: f"{r[2]}.{r[4] or primary_key(r[2])}"      # 열 생략 시 기본 키
               for r in db.execute(f"PRAGMA foreign_key_list({table})")}
        out.append(f"표 {table}")
        for _, col, typ, _, _, pk in db.execute(f"PRAGMA table_info({table})"):
            extra = " (기본 키)" if pk else (f" (→ {fks[col]})" if col in fks else "")
            note = NOTES.get(f"{table}.{col}")
            out.append(f"  - {col} {typ}{extra}" + (f": {note}" if note else ""))
    return "\n".join(out)

prompt = f"""너는 SQLite의 SELECT 문 하나만 쓰는 도우미다.
아래 표와 열만 쓰고, 없는 열은 지어내지 마라.

{schema_text()}

질문: 2026-10-12 출장의 식비 한도는?
SQL:"""
print(prompt)
print(f"\n(프롬프트 {len(prompt)}자)")
