from collections import deque

labels = {"국내 출장 규정": "규정", "법인카드 규정": "규정", "경비 정산 지침": "규정",
          "전자 결재 규정": "규정",
          "영업팀": "부서", "재무팀": "부서", "인사팀": "부서",
          "민지(1001)": "직원", "서연(1003)": "직원",
          "준호(1002)": "직원", "민지(1005)": "직원"}
props = {"준호(1002)": {"직급": "과장", "내선": "2210"},
         "민지(1001)": {"직급": "대리", "내선": "1103"}}
edges = [("국내 출장 규정", "담당", "재무팀"), ("법인카드 규정", "담당", "재무팀"),
         ("경비 정산 지침", "담당", "재무팀"), ("전자 결재 규정", "담당", "재무팀"),
         ("재무팀", "팀장", "준호(1002)"), ("영업팀", "팀장", "민지(1001)"),
         ("민지(1001)", "소속", "영업팀"), ("서연(1003)", "소속", "영업팀"),
         ("준호(1002)", "소속", "재무팀"), ("민지(1005)", "소속", "재무팀"),
         ("국내 출장 규정", "적용", "영업팀"), ("국내 출장 규정", "적용", "재무팀"),
         ("국내 출장 규정", "관련", "법인카드 규정"),
         ("법인카드 규정", "관련", "경비 정산 지침"),
         ("경비 정산 지침", "관련", "전자 결재 규정")]

def out(node, kind):                     # node에서 kind 관계로 나가는 이웃
    return [b for a, k, b in edges if a == node and k == kind]

def into(node, kind):                    # kind 관계로 node에 들어오는 이웃
    return [a for a, k, b in edges if b == node and k == kind]

rule = "국내 출장 규정"
print(f"① {rule}이 바뀌면 누구에게 물어보나?")
for dept in out(rule, "담당"):
    for who in out(dept, "팀장"):
        p = props[who]
        print(f"   {rule} -담당→ {dept} -팀장→ {who} ({p['직급']}, 내선 {p['내선']})")

print(f"② {rule}이 바뀌면 영향받는 직원은?")
affected = [who for dept in out(rule, "적용") for who in into(dept, "소속")]
print("   " + ", ".join(affected))

print(f"③ {rule}과 함께 봐야 할 규정은? (관련을 끝까지 따라가기)")
seen, queue = {rule}, deque([(rule, 0)])
while queue:
    node, depth = queue.popleft()
    for nxt in out(node, "관련"):
        if nxt not in seen:
            seen.add(nxt)
            queue.append((nxt, depth + 1))
            owner = out(nxt, "담당")[0]
            print(f"   {depth + 1}단계: {nxt} ({labels[nxt]}, 담당 {owner})")
