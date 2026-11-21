import re

manuals = {
    "AP-100": ("## 필터 청소\n1. 전원 플러그를 뽑는다.\n2. 뒤판을 연다.\n"
               "3. 필터를 물로 헹궈 말린다.\n"
               "## 소음이 날 때\n바닥이 평평한지 확인한다."),
    "AP-200": ("## 필터 청소\n1. 전원 버튼을 3초 누른다.\n2. 앞판을 연다.\n"
               "3. 필터를 솔로 턴다. 물로 씻지 않는다.\n"
               "## 소음이 날 때\n필터가 바르게 끼워졌는지 확인한다."),
}

cards = []                                   # 제목 단위로 자르고 모델 이름을 뒷면에 적는다
for model, text in manuals.items():
    for part in re.split(r"(?=^## )", text, flags=re.M):
        if part.strip():
            title, body = part[3:].split("\n", 1)
            cards.append({"모델": model, "제목": title, "본문": body.strip()})

print("30자씩 자르면 AP-200 설명서의 두 번째 조각:")
print("  " + manuals["AP-200"][30:60].replace("\n", " / "))
c = cards[2]
print(f"제목 단위로 자르면 카드 {len(cards)}장. 그중 하나:")
print(f"  앞면: {c['제목']}")
for line in c["본문"].split("\n"):
    print(f"        {line}")
print(f"  뒷면: 모델={c['모델']}")

def answer(question, use_model):
    pool = cards
    found = re.search(r"AP-\d+", question)
    if use_model and found:                  # 질문에 모델 이름이 있으면 그 모델 카드만
        pool = [c for c in cards if c["모델"] == found.group()]
    best = max(pool, key=lambda c: sum(w in question for w in c["제목"].split()))
    return f'[{best["모델"]}] {best["본문"].splitlines()[-1]}'

q = "AP-200 필터 청소 어떻게 해요?"
print(q)
print("  모델로 거르지 않으면 →", answer(q, False))
print("  모델로 거르면       →", answer(q, True))
