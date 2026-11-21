import sqlite3, json, math

# ① 관계형: 표로 정리하고 정확히 센다
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE 직원 (이름 TEXT, 부서 TEXT, 직급 TEXT)")
db.executemany("INSERT INTO 직원 VALUES (?, ?, ?)",
               [("민지", "영업팀", "대리"), ("준호", "재무팀", "과장"),
                ("서연", "영업팀", "사원")])
n = db.execute("SELECT COUNT(*) FROM 직원 WHERE 부서 = '영업팀'").fetchone()[0]
print(f"① 영업팀 인원: {n}명")

# ② 문서: 대화 한 건을 모양 그대로 통째로
doc = {"사용자": "민지", "날짜": "2026-11-20",
       "메시지": [{"role": "user", "content": "식비는요?"},
                  {"role": "assistant", "content": "하루 4만 원입니다."}]}
size = len(json.dumps(doc, ensure_ascii=False))
print(f"② 대화 문서: {doc['사용자']} 님, 메시지 {len(doc['메시지'])}개, {size}자")

# ③ 키-값(캐시): 이름표 하나로 바로 꺼낸다
cache = {"faq:연차": "1년 근무 시 15일 (취업 규칙 제4조)"}
print("③ 캐시에서 바로:", cache.get("faq:연차"))

# ④ 벡터: 뜻을 좌표로 바꿔 가장 가까운 것을 찾는다 (장난감 2차원)
vecs = {"식비 조항": (0.9, 0.1), "숙박비 조항": (0.7, 0.4), "연차 조항": (0.1, 0.9)}
q = (0.85, 0.15)   # "밥값 얼마예요?"의 좌표라고 가정
print("④ 뜻이 가장 가까운 것:", min(vecs, key=lambda k: math.dist(q, vecs[k])))

# ⑤ 그래프: 연결을 따라간다
edges = [("국내 출장 규정", "담당", "재무팀"), ("재무팀", "담당자", "준호"),
         ("국내 출장 규정", "관련", "법인카드 규정")]
step1 = next(b for a, r, b in edges if a == "국내 출장 규정" and r == "담당")
step2 = next(b for a, r, b in edges if a == step1 and r == "담당자")
print("⑤ 출장 규정 문의: 국내 출장 규정 →", step1, "→", step2)
