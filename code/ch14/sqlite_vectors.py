import sqlite3, json, math

def cosine(a_json, b_json):                  # SQL 안에서 부를 수 있는 벡터 함수
    a, b = json.loads(a_json), json.loads(b_json)
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

db = sqlite3.connect(":memory:")
db.create_function("cosine", 2, cosine)      # SQLite에 새 함수를 등록한다
db.executescript("""
CREATE TABLE 규정 (규정명 TEXT PRIMARY KEY, 담당부서 TEXT);
CREATE TABLE 카드 (id TEXT PRIMARY KEY, 규정명 TEXT REFERENCES 규정,
                   본문 TEXT, 시행일 TEXT, 종료일 TEXT, 공개 TEXT, 벡터 TEXT);
INSERT INTO 규정 VALUES ('국내 출장 규정', '재무팀'), ('임원 보수 규정', '인사팀');
""")
cards = [  # (id, 규정명, 본문, 시행일, 종료일, 공개, 벡터)
    ("출장-2-v1", "국내 출장 규정", "제2조(식비) 하루 3만 원까지",
     "2025-01-01", "2026-10-31", "전체", [0.9, 0.2, 0.0, 1.0, 0.0]),
    ("출장-2-v2", "국내 출장 규정", "제2조(식비) 하루 4만 원까지",
     "2026-11-01", None, "전체", [0.9, 0.2, 0.0, 1.0, 0.0]),
    ("출장-3", "국내 출장 규정", "제3조(숙박비) 하루 7만 원까지",
     "2025-01-01", None, "전체", [0.9, 0.5, 0.2, 0.0, 0.0]),
    ("보수-1", "임원 보수 규정", "임원 보수는 이사회가 정한다",
     "2025-01-01", None, "인사팀", [0.6, 0.0, 0.0, 0.0, 1.0])]
db.executemany("INSERT INTO 카드 VALUES (?, ?, ?, ?, ?, ?, ?)",
               [(*c[:6], json.dumps(c[6])) for c in cards])

q = json.dumps([0.8, 0.0, 0.0, 1.0, 0.0])    # 질문: 밥값 얼마까지 돼요?
rows = db.execute("""
    SELECT 카드.본문, 규정.담당부서, ROUND(cosine(카드.벡터, ?), 2) AS 점수
    FROM 카드 JOIN 규정 USING (규정명)
    WHERE 카드.시행일 <= ? AND (카드.종료일 IS NULL OR ? <= 카드.종료일)
      AND 카드.공개 IN ('전체', ?)
    ORDER BY 점수 DESC LIMIT 2""",
    (q, "2026-11-21", "2026-11-21", "영업팀")).fetchall()
for text, dept, score in rows:
    print(f"{score}  {text}  (문의: {dept})")
