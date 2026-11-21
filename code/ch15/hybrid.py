import math

cards = {  # 머리말을 붙인 본문(12.5절)과 장난감 좌표(돈, 이동, 쉼, 먹기, 인사)
    "제2조 식비": ("제2조(식비) 출장자에게 하루 4만 원까지 식비를 지급한다.",
        (0.9, 0.2, 0.0, 1.0, 0.0)),
    "제3조 숙박비": ("제3조(숙박비) 숙박비는 하루 7만 원까지 지급한다.",
        (0.9, 0.5, 0.2, 0.0, 0.0)),
    "제5조의2 별빛": ("제5조의2(별빛) 별빛 프로젝트 현장 출장은 교통비를 실비로 준다.",
        (0.5, 0.8, 0.0, 0.0, 0.4)),
    "제6조 영수증": ("제6조(분실) 영수증을 잃어버린 경우 사유서를 내면 지급한다.",
        (0.6, 0.1, 0.0, 0.3, 0.3)),
    "제8조 교통비": ("제8조(교통비) 출장 교통비는 대중교통 이용을 원칙으로 한다.",
        (0.6, 0.9, 0.0, 0.0, 0.0)),
    "취업 제4조 연차": ("제4조(연차) 1년 근무한 직원에게 연차 휴가 15일을 준다.",
        (0.0, 0.0, 0.9, 0.0, 0.3)),
}

def grams(text):                             # 두 글자씩 자른 낱말 조각
    t = "".join(ch for ch in text if ch.isalnum())
    return [t[i:i + 2] for i in range(len(t) - 1)]

def bm25(query, k1=1.2, b=0.75):             # 글자로 찾기: BM25 점수
    docs = {n: grams(text) for n, (text, _) in cards.items()}
    avg = sum(len(d) for d in docs.values()) / len(docs)
    score = {}
    for name, d in docs.items():
        s = 0.0
        for g in set(grams(query)):
            n = sum(g in other for other in docs.values())        # 이 조각이 든 카드 수
            if n == 0 or g not in d:
                continue
            idf = math.log((len(docs) - n + 0.5) / (n + 0.5) + 1)  # 드물수록 크다
            tf = d.count(g)
            s += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * len(d) / avg))
        score[name] = s
    return sorted(score, key=score.get, reverse=True)

def by_vector(qvec):                          # 뜻으로 찾기: 코사인
    def cos(a, c):
        dot = sum(x * y for x, y in zip(a, c))
        return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in c)))
    return sorted(cards, key=lambda n: cos(qvec, cards[n][1]), reverse=True)

def rrf(*rankings, k=60):                     # 순위 섞기: 1/(k + 등수)를 더한다
    score = {}
    for ranking in rankings:
        for r, name in enumerate(ranking, start=1):
            score[name] = score.get(name, 0) + 1 / (k + r)
    return sorted(score, key=score.get, reverse=True)

questions = [("밥값 얼마까지 돼요?", (0.8, 0.0, 0.0, 1.0, 0.0), "제2조 식비"),
             ("별빛 프로젝트 출장비는요?", (0.6, 0.9, 0.0, 0.0, 0.0), "제5조의2 별빛"),
             ("영수증 잃어버리면 어떡해요?", (0.7, 0.1, 0.0, 0.2, 0.0), "제6조 영수증")]
for q, qvec, want in questions:
    kw, vec = bm25(q), by_vector(qvec)
    mix = rrf(kw, vec)
    print(f"{q}  (정답: {want})")
    for name, r in [("글자 BM25", kw), ("뜻 벡터 ", vec), ("섞기 RRF", mix)]:
        mark = "✓" if r[0] == want else "✕"
        print(f"  {name}: {mark} 1등 {r[0]} · 정답은 {r.index(want) + 1}등")
