import math
from datetime import date

# 규정 도우미가 겪은 일 한 편씩 (좌표 축: 영수증, 식비·한도, 교통, 정산)
episodes = [
 {"날짜": date(2026, 11, 3), "범위": "공용", "중요도": 8, "좌표": (0.9, 0, 0.4, 0.2),
  "상황": "출장 중 택시 영수증을 잃어버린 직원",
  "결과": "사유서 양식을 몰라 다시 물어봄",
  "교훈": "제6조와 함께 사유서 양식 위치(재무팀 게시판)를 알려 준다"},
 {"날짜": date(2026, 11, 18), "범위": "공용", "중요도": 9, "좌표": (0, 0.9, 0, 0.5),
  "상황": "10월 출장 식비를 새 한도로 안내",
  "결과": "출장 날짜 기준 3만 원이 맞아 정정",
  "교훈": "정산 질문에는 출장 날짜를 먼저 확인한다"},
 {"날짜": date(2026, 10, 2), "범위": "공용", "중요도": 4, "좌표": (0.6, 0, 0.7, 0.3),
  "상황": "KTX 영수증 대신 카드 내역을 내도 되는지",
  "결과": "그대로 처리됨",
  "교훈": "카드 매출 전표로 대신할 수 있다"},
 {"날짜": date(2026, 11, 20), "범위": 1001, "중요도": 3, "좌표": (0.5, 0.6, 0.2, 0.1),
  "상황": "민지 님의 부산 출장 식비 질문",
  "결과": "이틀 치 8만 원으로 안내",
  "교훈": "1박 2일이면 식비를 이틀 치로 계산해 준다"}]

def cos(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.hypot(*a) * math.hypot(*b))

def recall(qvec, emp, today, k=1):
    scored = []
    for e in episodes:
        if e["범위"] not in ("공용", emp):        # 남의 개인 에피소드는 건너뛴다
            continue
        rel = cos(qvec, e["좌표"])                    # 관련도: 11장의 코사인
        near = 0.99 ** (today - e["날짜"]).days       # 가까움: 하루 지날 때마다 1%씩
        imp = e["중요도"] / 10                        # 중요도: 1~10을 0.1~1로
        scored.append((rel + near + imp, rel, near, imp, e))
    scored.sort(key=lambda s: s[0], reverse=True)
    for total, rel, near, imp, e in scored:
        mark = "✕" if rel < 0.8 else " "              # 11장의 기준선 0.8
        print(f"{mark} {total:.2f} = 관련 {rel:.2f} + 가까움 {near:.2f}"
              f" + 중요 {imp:.1f}  {e['상황']}")
    return [s[4] for s in scored if s[1] >= 0.8][:k]

q = "출장 가서 택시 영수증을 잃어버렸는데 어떻게 해요?"
print("질문:", q, "(서연, 1003)")
for e in recall((0.9, 0, 0.4, 0.3), 1003, date(2026, 11, 21)):
    print(f"→ 작업대에: [{e['날짜']}] {e['상황']}")
    print(f"   교훈: {e['교훈']}")
