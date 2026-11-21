# 규정 DB를 MCP 서버로 내놓는다. 클라이언트가 이 파일을 따로 실행해 대화한다.
import sqlite3
from tiny_mcp import schema, serve

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE 조항 (규정 TEXT, 번호 TEXT, 제목 TEXT, 내용 TEXT)")
db.executemany("INSERT INTO 조항 VALUES (?, ?, ?, ?)", [
    ("국내 출장 규정", "제2조", "식비", "하루 4만 원까지 식비를 지급한다."),
    ("국내 출장 규정", "제3조", "숙박비", "숙박비는 하루 7만 원까지 지급한다."),
    ("국내 출장 규정", "제6조", "분실", "영수증을 잃어버리면 사유서를 내고 받는다."),
    ("취업 규칙", "제4조", "연차", "1년 근무한 직원에게 연차 휴가 15일을 준다.")])

def search_rules(keyword):                      # 정해 둔 SELECT만 실행한다
    rows = db.execute("SELECT 규정, 번호, 제목, 내용 FROM 조항 WHERE 제목 LIKE ? "
                      "OR 내용 LIKE ? LIMIT 3", (f"%{keyword}%",) * 2).fetchall()
    return "\n".join(f"{r} {n}({t}) {c}" for r, n, t, c in rows) or "찾은 조항 없음"

def get_article(rule, number):
    row = db.execute("SELECT 제목, 내용 FROM 조항 WHERE 규정 = ? AND 번호 = ?",
                     (rule, number)).fetchone()
    if row is None:
        raise ValueError(f"{rule} {number}는 없다")
    return f"{rule} {number}({row[0]}) {row[1]}"

serve("regulations", {
    "search_rules": ("회사 규정에서 낱말이 들어간 조항을 3개까지 찾는다.",
                     schema("keyword"), search_rules),
    "get_article": ("규정 이름과 조항 번호로 조항 하나의 원문을 가져온다.",
                    schema("rule", "number"), get_article)})
