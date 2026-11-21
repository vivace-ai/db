import math, random

random.seed(13)
centers = [[random.uniform(0, 10) for _ in range(8)] for _ in range(30)]
cards = [[c + random.gauss(0, 0.8) for c in random.choice(centers)] for _ in range(20000)]
questions = [[c + random.gauss(0, 0.8) for c in random.choice(centers)] for _ in range(50)]

def nearest(q, pool):                       # pool에서 q와 가장 가까운 카드 번호
    return min(pool, key=lambda i: math.dist(q, cards[i]))

# 동네 나누기: 대표점 64개를 정하고, 카드마다 가장 가까운 대표점의 동네에 넣는다
reps = random.sample(cards, 64)
for _ in range(3):                          # 대표점을 동네의 한가운데로 세 번 옮긴다
    towns = [[] for _ in reps]
    for i, v in enumerate(cards):
        towns[min(range(len(reps)), key=lambda t: math.dist(v, reps[t]))].append(i)
    reps = [[sum(cards[i][d] for i in t) / len(t) for d in range(8)] if t else r
            for t, r in zip(towns, reps)]

answer = [nearest(q, range(len(cards))) for q in questions]      # 전부 비교한 정답
print(f"전부 비교: 질문마다 {len(cards):,}번 비교, 정답률 100%")
for nprobe in [1, 3, 8]:
    hits = comps = 0
    for q, truth in zip(questions, answer):
        near_towns = sorted(range(len(reps)), key=lambda t: math.dist(q, reps[t]))[:nprobe]
        pool = [i for t in near_towns for i in towns[t]]
        comps += len(reps) + len(pool)
        hits += nearest(q, pool) == truth
    print(f"동네 {nprobe}곳만: 질문마다 약 {comps // len(questions):,}번 비교, "
          f"정답률 {hits / len(questions):.0%}")
