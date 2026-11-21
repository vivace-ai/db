import math, random

random.seed(13)
centers = [[random.uniform(0, 10) for _ in range(8)] for _ in range(30)]
cards = [[c + random.gauss(0, 0.8) for c in random.choice(centers)] for _ in range(3000)]
questions = [[c + random.gauss(0, 0.8) for c in random.choice(centers)] for _ in range(100)]

def link(members, k):                       # 층 안에서 길을 놓는다
    roads = {}
    for i in members:
        near = sorted(members, key=lambda j: math.dist(cards[i], cards[j]))[1:k + 1]
        near += random.sample(members, 2)    # 먼 곳으로 가는 긴 길 2개
        roads.setdefault(i, set()).update(near)
        for j in near:
            roads.setdefault(j, set()).add(i)   # 길은 양쪽으로
    return roads

everyone = list(range(len(cards)))
floors = [link(everyone, 6),                # 1층 골목길: 모든 카드
          link(everyone[::10], 5),          # 2층 국도: 10장에 1장
          link(everyone[::100], 4)]         # 3층 고속도로: 100장에 1장

def search(q, ef):
    memo = {}                               # 거리를 잰 카드 (= 비교 횟수)
    def d(i):
        if i not in memo:
            memo[i] = math.dist(q, cards[i])
        return memo[i]
    here = 0                                # 3층의 정해진 출발점
    for roads in floors[:0:-1]:             # 3층, 2층: 더 가까워지는 쪽으로만 간다
        moved = True
        while moved:
            moved = False
            for j in roads[here]:
                if d(j) < d(here):
                    here, moved = j, True
    best, todo, seen = [here], [here], {here}   # 1층: 후보를 ef개까지 들고 살핀다
    while todo:
        cur = min(todo, key=d)
        todo.remove(cur)
        if len(best) >= ef and d(cur) > d(best[-1]):
            break                           # 더 살펴도 나아질 것이 없다
        for j in floors[0][cur]:
            if j not in seen:
                seen.add(j)
                todo.append(j)
                best = sorted(best + [j], key=d)[:ef]
    return best[0], len(memo)

answer = [min(everyone, key=lambda i: math.dist(q, cards[i])) for q in questions]
print(f"전부 비교: 질문마다 {len(cards):,}번, 정답률 100%")
for ef in [1, 4, 16]:
    results = [search(q, ef) for q in questions]
    hits = sum(r == a for (r, _), a in zip(results, answer))
    comps = sum(c for _, c in results) // len(questions)
    print(f"ef={ef:>2}: 질문마다 약 {comps}번 비교, 정답률 {hits / len(questions):.0%}")
