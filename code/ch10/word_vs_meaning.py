import math

docs = {"식비 조항":   "국내 출장 시 식비는 하루 4만 원까지 지급한다.",
        "숙박비 조항": "국내 출장 시 숙박비는 하루 7만 원까지 지급한다.",
        "연차 조항":   "1년 근무한 직원에게 연차 휴가 15일을 준다.",
        "법인카드 조항": "법인카드는 업무 목적에만 사용한다."}

# 장난감 임베딩: 낱말마다 사람이 정한 네 축의 좌표 (돈, 이동, 쉼, 먹기)
words = {"식비": (0.9, 0.2, 0.0, 1.0),   "밥값": (0.8, 0.0, 0.0, 1.0),
         "점심": (0.1, 0.0, 0.1, 0.8),   "숙박비": (0.9, 0.5, 0.2, 0.0),
         "호텔": (0.4, 0.5, 0.4, 0.0),   "연차": (0.0, 0.0, 0.9, 0.0),
         "휴가": (0.0, 0.1, 0.9, 0.0),   "쉴": (0.0, 0.0, 0.8, 0.0),
         "며칠": (0.0, 0.0, 0.4, 0.0),   "출장": (0.2, 0.9, 0.0, 0.0),
         "법인카드": (0.5, 0.1, 0.0, 0.0), "업무": (0.1, 0.2, 0.0, 0.0),
         "얼마": (0.7, 0.0, 0.0, 0.0),   "지급": (0.7, 0.0, 0.0, 0.0)}

def embed(text):                      # 문장에 들어 있는 낱말 좌표의 평균
    found = [v for w, v in words.items() if w in text]
    return tuple(round(sum(axis) / len(found), 2) for axis in zip(*found))

def bigrams(text):                    # 두 글자씩 묶음: "밥값 얼마" → {밥값, 값얼, 얼마}
    t = text.replace(" ", "")
    return {t[i:i + 2] for i in range(len(t) - 1)}

def by_letters(q):                    # 겹치는 글자 묶음이 가장 많은 조항
    score = {name: len(bigrams(q) & bigrams(d)) for name, d in docs.items()}
    best = max(score.values())
    return [n for n, s in score.items() if s == best and s > 0], best

def by_meaning(q):                    # 좌표가 가까운 순서로 조항을 줄 세운다
    qv = embed(q)
    near = sorted((round(math.dist(qv, embed(d)), 2), n) for n, d in docs.items())
    return near, qv

for q in ["밥값 얼마까지 돼요?", "호텔비는 얼마나 나와요?", "며칠 쉴 수 있어요?"]:
    names, n = by_letters(q)
    near, qv = by_meaning(q)
    (d1, first), (d2, second) = near[0], near[1]
    print(f"질문: {q}  좌표 {qv}")
    print(f"  글자로 찾기 → {' / '.join(names) or '못 찾음'} (겹친 글자 묶음 {n}개)")
    print(f"  뜻으로 찾기 → {first} (거리 {d1}), 다음은 {second} ({d2})")
