import sqlite3, json

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE 상품 (상품번호 INTEGER PRIMARY KEY, "
           "문서 TEXT NOT NULL CHECK (json_valid(문서)))")
items = [
    {"이름": "기본 티셔츠", "가격": 19000, "사이즈": ["S", "M", "L"], "색상": ["흰색", "검정"]},
    {"이름": "가벼운 노트북", "가격": 1290000, "사양": {"메모리GB": 16, "무게kg": 1.1}},
    {"이름": "게임 노트북", "가격": 2190000, "사양": {"메모리GB": 32, "무게kg": 2.4}},
    {"이름": "여행 에세이", "가격": 16800, "저자": "김하늘", "쪽수": 240},
    {"이름": "후드 집업", "가격": 49000, "사이즈": ["M", "XL"]},
]
db.executemany("INSERT INTO 상품 (문서) VALUES (?)",
               [(json.dumps(i, ensure_ascii=False),) for i in items])

print("상품마다 가진 칸:")
for (doc,) in db.execute("SELECT 문서 FROM 상품"):
    d = json.loads(doc)
    print(f"  {d['이름']}: {', '.join(k for k in d if k != '이름')}")

light = db.execute("SELECT json_extract(문서, '$.이름') FROM 상품 "
                   "WHERE json_extract(문서, '$.사양.무게kg') <= 1.5").fetchall()
print("1.5kg 이하 노트북:", [n for (n,) in light])

m = db.execute("SELECT json_extract(상품.문서, '$.이름') FROM 상품, "
               "json_each(상품.문서, '$.사이즈') AS s WHERE s.value = 'M' "
               "ORDER BY 상품번호").fetchall()
print("M 사이즈가 있는 상품:", [n for (n,) in m])

db.execute("INSERT INTO 상품 (문서) VALUES (?)", (json.dumps(
    {"이름": "원두 200g", "가격": 15000, "로스팅": "중배전"}, ensure_ascii=False),))
count = db.execute("SELECT COUNT(*) FROM 상품").fetchone()[0]
print(f"새 모양의 상품도 표를 고치지 않고 넣었다: 모두 {count}개")
