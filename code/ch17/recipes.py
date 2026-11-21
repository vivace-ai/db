parent = {"두부": "콩 가공품", "된장": "콩 가공품", "간장": "콩 가공품",
          "콩 가공품": "콩류", "새우": "갑각류", "게": "갑각류",
          "갑각류": "해산물", "오징어": "해산물"}
recipes = {"김치찌개": ["돼지고기", "김치", "두부"], "된장찌개": ["애호박", "된장"],
           "새우볶음밥": ["밥", "새우", "달걀"],
           "간장 불고기": ["소고기", "간장", "양파"],
           "오징어볶음": ["오징어", "양파", "고춧가루"], "달걀말이": ["달걀", "대파"]}

def ancestors(food):                     # 재료에서 위로 올라가며 만나는 모든 개념
    out = []
    while food in parent:
        food = parent[food]
        out.append(food)
    return out

def safe_for(allergy, by_name_only):
    ok = []
    for dish, foods in recipes.items():
        if by_name_only:                 # 재료 이름에 '콩'이라는 글자가 있는지만 본다
            bad = [f for f in foods if allergy.rstrip("류") in f]
        else:                            # 온톨로지: 재료의 위 개념까지 따라간다
            bad = [f for f in foods if allergy in [f] + ancestors(f)]
        if not bad:
            ok.append(dish)
    return ok

print("두부의 위 개념:", " → ".join(["두부"] + ancestors("두부")))
for allergy in ["콩류", "갑각류"]:
    print(f"{allergy} 알레르기가 있는 사람이 먹을 수 있는 요리")
    for name, by_name in [("글자로만", True), ("온톨로지로", False)]:
        ok = safe_for(allergy, by_name)
        out = [d for d in recipes if d not in ok]
        print(f"  {name} 거르면: {len(ok)}개 통과 · 빠짐: {', '.join(out) or '없음'}")
