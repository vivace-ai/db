import math

def dot(a, b):                       # 내적: 축마다 곱해서 모두 더한다
    return sum(x * y for x, y in zip(a, b))

def length(a):                       # 화살표의 길이
    return math.sqrt(dot(a, a))

def cosine(a, b):                    # 코사인 유사도: 방향이 얼마나 같은가
    return dot(a, b) / (length(a) * length(b))

def unit(a):                         # 길이를 1로 맞춘다(정규화)
    return tuple(x / length(a) for x in a)

# 네 축 (돈, 이동, 쉼, 먹기). 긴 안내문은 짧은 조항과 방향은 같고 길이만 3배
q = (0.8, 0.0, 0.0, 1.0)                           # 질문: 밥값 얼마까지 돼요?
docs = {"식비 조항":     (0.9, 0.2, 0.0, 1.0),
        "식비 긴 안내문": (2.7, 0.6, 0.0, 3.0),
        "숙박비 조항":   (0.9, 0.5, 0.2, 0.0),
        "연차 조항":     (0.0, 0.0, 0.9, 0.0)}

for name, d in docs.items():
    print(f"{name}: 거리 {math.dist(q, d):.2f} · 코사인 {cosine(q, d):.2f}"
          f" · 내적 {dot(q, d):.2f}")

def rank(score, big_first):          # 점수로 줄 세운 문서 이름들
    return sorted(docs, key=lambda n: score(docs[n]), reverse=big_first)

print("거리 순위  :", rank(lambda d: math.dist(q, d), False))
print("코사인 순위:", rank(lambda d: cosine(q, d), True))
print("내적 순위  :", rank(lambda d: dot(q, d), True))

docs = {n: unit(d) for n, d in docs.items()}       # 모두 길이 1로 맞춘 뒤
q = unit(q)
print("길이 1로 맞춘 뒤 거리 순위:", rank(lambda d: math.dist(q, d), False))
print("길이 1로 맞춘 뒤 내적 순위:", rank(lambda d: dot(q, d), True))
