from collections import deque

# 가상의 경제 뉴스 세 건 (회사와 사람은 모두 지어낸 것)과, 기사마다 뽑은 사실
articles = {
    "기사 1": [("한빛전자", "인수", "누리소프트"), ("누리소프트", "대표", "강서진")],
    "기사 2": [("강서진", "전 직장", "바다물산"), ("바다물산", "협력", "푸른배터리")],
    "기사 3": [("푸른배터리", "공급", "한빛전자"), ("한빛전자", "대표", "오태민")],
}
near = {}
for src, facts in articles.items():
    for a, rel, b in facts:
        near.setdefault(a, []).append((rel, b, src))
        near.setdefault(b, []).append((rel, a, src))      # 거꾸로도 따라갈 수 있게

def path(start, goal):                                  # 16장의 너비 우선 탐색
    back, queue = {start: None}, deque([start])
    while queue:
        cur = queue.popleft()
        for rel, nxt, src in near[cur]:
            if nxt not in back:
                back[nxt] = (cur, rel, src)
                queue.append(nxt)
    steps, node = [], goal
    while back[node]:
        prev, rel, src = back[node]
        steps.insert(0, f"{prev} -{rel}- {node} ({src})")
        node = prev
    return steps

for a, b in [("누리소프트", "바다물산"), ("오태민", "강서진")]:
    one = [s for s, facts in articles.items()
           if {a, b} <= {x for f in facts for x in (f[0], f[2])}]
    print(f"{a} ↔ {b}: 두 이름이 함께 나온 기사 {len(one)}건")
    for step in path(a, b):
        print("   " + step)
