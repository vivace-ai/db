import math

def cos(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

# 4부의 카드: 본문과 장난감 좌표(돈, 이동, 쉼, 먹기, 인사)
cards = {"국내 출장 규정": ("제2조(식비) 하루 4만 원, 제3조(숙박비) 하루 7만 원",
                        (0.9, 0.6, 0, 0.5, 0)),
         "법인카드 규정": ("업무에만 쓰고 영수증을 첨부한다", (0.8, 0.1, 0, 0.1, 0)),
         "경비 정산 지침": ("출장 후 7일 안에 정산한다", (0.7, 0.3, 0, 0, 0)),
         "취업 규칙": ("제4조(연차) 1년 근무 시 15일", (0, 0, 0.9, 0, 0.4))}
# 5부의 그래프: 규정 사이의 관계와 조직도 (16·17장)
edges = [("국내 출장 규정", "담당", "재무팀"),
         ("재무팀", "팀장", "준호(내선 2210)"),
         ("국내 출장 규정", "관련", "법인카드 규정"),
         ("법인카드 규정", "관련", "경비 정산 지침"),
         ("취업 규칙", "담당", "인사팀"), ("인사팀", "팀장", "도윤(내선 3105)")]

def neighbors(node, hops):                  # node에서 hops단계 안의 사실들
    found, frontier = [], {node}
    for _ in range(hops):
        step = [e for e in edges if e[0] in frontier and e not in found]
        found += step
        frontier = {b for _, _, b in step}
    return found

q = "출장 규정 바뀌면 누구한테 물어보고, 같이 봐야 할 규정은 뭐예요?"
qvec = (0.8, 0.6, 0, 0.2, 0)
start = max(cards, key=lambda n: cos(qvec, cards[n][1]))        # ① 뜻으로 시작점 찾기
print(f"질문: {q}")
print(f"① 벡터 검색 1등: {start} ({cos(qvec, cards[start][1]):.2f})")
print("② 벡터만 쓴 작업대:")
print(f"   [{start}] {cards[start][0]}")
print("③ 그래프로 넓힌 작업대:")
print(f"   [{start}] {cards[start][0]}")
for a, rel, b in neighbors(start, 2):                           # ② 관계를 따라 넓히기
    print(f"   {a} -{rel}→ {b}")
