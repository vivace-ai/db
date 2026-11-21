import math

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

# 카드 = 본문 + 좌표(돈, 이동, 쉼, 먹기, 인사) + 메타데이터(카드 뒷면)
cards = [
    {"id": "출장-2-v1", "text": "제2조(식비) 하루 3만 원까지",
     "vec": (0.9, 0.2, 0.0, 1.0, 0.0),
     "시행일": "2025-01-01", "종료일": "2026-10-31", "공개": "전체"},
    {"id": "출장-2-v2", "text": "제2조(식비) 하루 4만 원까지",
     "vec": (0.9, 0.2, 0.0, 1.0, 0.0),
     "시행일": "2026-11-01", "종료일": None, "공개": "전체"},
    {"id": "출장-3", "text": "제3조(숙박비) 하루 7만 원까지",
     "vec": (0.9, 0.5, 0.2, 0.0, 0.0),
     "시행일": "2025-01-01", "종료일": None, "공개": "전체"},
    {"id": "보수-1", "text": "임원 보수는 이사회가 정한다",
     "vec": (0.6, 0.0, 0.0, 0.0, 1.0),
     "시행일": "2025-01-01", "종료일": None, "공개": "인사팀"},
]

def usable(card, today, team):              # 카드 뒷면으로 거르는 조건
    started = card["시행일"] <= today
    not_ended = card["종료일"] is None or today <= card["종료일"]
    in_force = started and not_ended
    return in_force and card["공개"] in ("전체", team)

def search(qvec, today=None, team=None):
    pool = [c for c in cards if today is None or usable(c, today, team)]
    best = max(pool, key=lambda c: cosine(qvec, c["vec"]))
    score = cosine(qvec, best["vec"])
    if score < 0.8:                         # 11장의 기준선
        return f"찾지 못함 (가장 가까운 {best['id']}도 {score:.2f})"
    return f'{best["text"]} ({best["id"]}, {score:.2f})'

meal, pay = (0.8, 0.0, 0.0, 1.0, 0.0), (0.5, 0.0, 0.0, 0.0, 1.0)
print("밥값 얼마까지 돼요?")
print("  거르지 않으면 →", search(meal))
print("  거르면       →", search(meal, "2026-11-21", "영업팀"))
print("임원 보수 얼마예요? (영업팀 직원)")
print("  거르지 않으면 →", search(pay))
print("  거르면       →", search(pay, "2026-11-21", "영업팀"))
