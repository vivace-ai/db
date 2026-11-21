import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from agent import run

def limit(item, date):
    return [("limit", {"item": item, "date": date})]

# 평가 질문 묶음(15장): (질문, LLM이 세운 계획의 예, 작업대에 꼭 올라와야 할 근거)
tests = [("10월 12일 출장 식비 한도는?",
          limit("식비 한도", "2026-10-12"), "하루 3만 원"),
         ("11월 25일 출장 식비 한도는?",
          limit("식비 한도", "2026-11-25"), "하루 4만 원"),
         ("숙박비는 얼마까지 돼요?",
          limit("숙박비 한도", "2026-11-21"), "하루 7만 원"),
         ("영수증 잃어버리면요?",
          [("search_cards", {"qvec": [0.2, 0, 0.9, 0]})], "제6조"),
         ("출장 규정 담당자는요?",
          [("find_owner", {"rule": "국내 출장 규정"})], "내선 2210"),
         ("지난달 출장 식비 얼마였어요?",                # 오늘은 2026-11-21
          limit("식비 한도", "2026-11-21"), "하루 3만 원")]

passed = 0
for question, tools, expect in tests:
    plan = {"좌표": [0.5, 0.5, 0, 0], "도구": tools}
    desk = run(1003, question, plan, show=False)
    ok = expect in desk["근거"]
    passed += ok
    print(f"{'✓' if ok else '✕'} {question}  (기대: {expect})")
    if not ok:
        print(f"   작업대의 근거: {desk['근거']}")
print(f"{passed}/{len(tests)} 통과")
