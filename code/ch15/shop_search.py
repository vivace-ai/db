import math, re

def cos(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

# 상품: 이름, 색, 재고 있는 사이즈, 장난감 좌표(운동, 격식, 야외, 빨강)
items = [("런닝 운동화", "빨강", [250, 260, 270], (0.95, 0.05, 0.45, 0.55)),
         ("런닝 운동화", "파랑", [270, 280], (0.95, 0.05, 0.45, 0.0)),
         ("캔버스 운동화", "빨강", [230, 240], (0.88, 0.12, 0.3, 0.62)),
         ("하이힐", "빨강", [230, 240, 250], (0.1, 0.95, 0.1, 0.8)),
         ("등산화", "빨강", [260, 270, 280], (0.7, 0.1, 0.9, 0.6))]
COLORS = {"빨간": "빨강", "빨강": "빨강", "파란": "파랑", "파랑": "파랑"}

q, qvec = "빨간 운동화 270", (0.9, 0.1, 0.3, 0.6)

best = max(items, key=lambda it: cos(qvec, it[3]))             # ① 뜻으로만
print(f"① 뜻으로만: {best[1]} {best[0]} (재고 {best[2]})")

size = [int(n) for n in re.findall(r"\d{3}", q)]               # ② 질문을 나눈다
color = [COLORS[w] for w in q.split() if w in COLORS]
words = [w for w in q.split() if w not in COLORS and not w.isdigit()]
print(f"② 질문 나누기: 사이즈={size} 색={color} 나머지={words}")

pool = [it for it in items
        if all(s in it[2] for s in size) and all(c == it[1] for c in color)]
pool.sort(key=lambda it: (sum(w in it[0] for w in words), cos(qvec, it[3])), reverse=True)
for it in pool:
    print(f"   후보: {it[1]} {it[0]} (재고 {it[2]}, 뜻 점수 {cos(qvec, it[3]):.2f})")
print(f"③ 답: {pool[0][1]} {pool[0][0]} 270 재고 있음")
