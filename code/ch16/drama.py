from collections import deque

# 가상의 드라마 인물관계도 (인물은 모두 지어낸 것). 관계는 양쪽으로 통한다
ties = [("서윤", "친구", "지아"), ("지아", "남매", "태오"), ("태오", "라이벌", "하준"),
        ("하준", "연인", "은재"), ("서윤", "동료", "도하"), ("도하", "형제", "민결"),
        ("민결", "친구", "하준"), ("서윤", "동창", "은재")]
near = {}
for a, kind, b in ties:
    near.setdefault(a, []).append((kind, b))
    near.setdefault(b, []).append((kind, a))

def how_known(start, goal):              # 가장 짧은 연결 고리 찾기 (너비 우선)
    back, queue = {start: None}, deque([start])
    while queue:
        cur = queue.popleft()
        for kind, nxt in near[cur]:
            if nxt not in back:
                back[nxt] = (cur, kind)
                queue.append(nxt)
    chain, node = [goal], goal
    while back[node]:
        prev, kind = back[node]
        chain[:0] = [prev, f"-{kind}-"]
        node = prev
    return " ".join(chain)

def within(start, steps):                # start에서 steps단계 안의 사람들
    found, frontier = {start: 0}, [start]
    for step in range(1, steps + 1):
        frontier = [b for a in frontier for _, b in near[a] if b not in found]
        for b in frontier:
            found.setdefault(b, step)
    return {n: s for n, s in found.items() if s > 0}

print("서윤과 하준은 어떻게 아는 사이?", how_known("서윤", "하준"))
print("서윤에게서 2단계 안:", within("서윤", 2))
rivals = [r for kind, r in near["하준"] if kind == "라이벌"]
rival_sib = [b for r in rivals for kind, b in near[r] if kind == "남매"]
print("하준의 라이벌의 남매:", rival_sib)
