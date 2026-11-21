import math

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

docs = {"식비 조항": (0.9, 0.2, 0.0, 1.0), "숙박비 조항": (0.9, 0.5, 0.2, 0.0),
        "연차 조항": (0.0, 0.0, 0.9, 0.0)}
questions = {"밥값 얼마까지 돼요?": (0.8, 0.0, 0.0, 1.0),
             "주차장 몇 대예요?":   (0.1, 0.4, 0.0, 0.0)}   # 규정집에 없는 이야기
LIMIT = 0.8                                             # 이보다 낮으면 '관련 없음'

for q, qv in questions.items():
    best = max(docs, key=lambda n: cosine(qv, docs[n]))
    score = cosine(qv, docs[best])
    answer = best if score >= LIMIT else "관련 조항을 찾지 못했습니다"
    print(f"{q} → 가장 가까운 것: {best} ({score:.2f}) → 답: {answer}")
