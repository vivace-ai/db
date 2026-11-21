import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE 관계 (출발 TEXT, 종류 TEXT, 도착 TEXT)")   # 선 하나 = 줄 하나
db.executemany("INSERT INTO 관계 VALUES (?, ?, ?)", [
    ("국내 출장 규정", "담당", "재무팀"), ("재무팀", "팀장", "준호(1002)"),
    ("국내 출장 규정", "관련", "법인카드 규정"),
    ("법인카드 규정", "관련", "경비 정산 지침"),
    ("경비 정산 지침", "관련", "전자 결재 규정")])

# ① 두 단계 따라가기: 단계마다 표를 한 번씩 더 잇는다
row = db.execute("""SELECT a.도착, b.도착 FROM 관계 a JOIN 관계 b ON b.출발 = a.도착
                    WHERE a.출발 = '국내 출장 규정' AND a.종류 = '담당'
                      AND b.종류 = '팀장'""").fetchone()
print("① 담당 부서와 팀장:", row)

# ② 몇 단계인지 모를 때: 자기 자신을 다시 부르는 재귀 질문
rows = db.execute("""WITH RECURSIVE 연쇄(규정, 단계) AS (
                         SELECT '국내 출장 규정', 0
                         UNION
                         SELECT 관계.도착, 연쇄.단계 + 1 FROM 관계 JOIN 연쇄
                         ON 관계.출발 = 연쇄.규정 AND 관계.종류 = '관련')
                     SELECT 단계, 규정 FROM 연쇄
                     WHERE 단계 > 0 ORDER BY 단계""").fetchall()
for depth, name in rows:
    print(f"② {depth}단계 관련 규정: {name}")
