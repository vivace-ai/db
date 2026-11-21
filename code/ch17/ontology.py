# ① 개념(클래스)과 그 위의 개념: "팀장은 직원이다", "직원은 사람이다"
parent = {"팀장": "직원", "직원": "사람", "외부 강사": "사람",
          "비용 규정": "규정", "인사 규정": "규정"}
# ② 관계의 약속: 어떤 종류에서 어떤 종류로 가는가 (출발 → 도착)
relations = {"담당": ("규정", "부서"), "소속": ("직원", "부서"), "팀장": ("부서", "팀장")}
synonyms = {"관리": "담당", "책임": "담당", "근무": "소속"}   # ③ 같은 뜻의 다른 이름

def is_a(kind, target):                  # kind가 target의 한 종류인가 (위로 올라간다)
    while kind:
        if kind == target:
            return True
        kind = parent.get(kind)
    return False

kinds = {"준호": "팀장", "서연": "직원", "재무팀": "부서", "영업팀": "부서",
         "국내 출장 규정": "비용 규정", "김 강사": "외부 강사"}

def add(a, rel, b):                       # 약속을 지키는 관계만 받는다
    rel = synonyms.get(rel, rel)
    if rel not in relations:
        return f"✕ {a} -{rel}→ {b}: 약속에 없는 관계"
    need_a, need_b = relations[rel]
    if not is_a(kinds[a], need_a) or not is_a(kinds[b], need_b):
        return f"✕ {a} -{rel}→ {b}: {rel}은 {need_a} → {need_b}여야 한다"
    return f"✓ {a} -{rel}→ {b}"

for a, rel, b in [("국내 출장 규정", "관리", "재무팀"), ("준호", "근무", "재무팀"),
                  ("김 강사", "소속", "재무팀"), ("재무팀", "담당", "국내 출장 규정"),
                  ("서연", "친구", "준호")]:
    print(add(a, rel, b))

print("준호는 사람인가?", is_a(kinds["준호"], "사람"))
print("김 강사는 직원인가?", is_a(kinds["김 강사"], "직원"))
