import json, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))  # 같은 폴더의 stores.py
from stores import TOOLS, cos, episodes, long_term

RULES = "근거 조항을 붙인다. 규정에 없는 것은 지어내지 않고 담당 부서를 안내한다."
BUDGET = {"절차": 60, "장기": 30, "근거": 200, "에피소드": 40, "단기": 60}
cache = {}                         # 도구 결과 포스트잇(9장): 누가 물어도 같은 사실만

def run(emp, question, plan, show=True):
    say = print if show else (lambda *args: None)
    desk = {"절차": RULES}
    desk["장기"] = ", ".join(f"{k}: {v}" for k, v in long_term.get(emp, {}).items())
    desk["에피소드"] = " / ".join(t for t, v in episodes
                                 if cos(plan["좌표"], v) >= 0.8)    # 11장 기준선
    say(f"① 장기 기억: {desk['장기'] or '없음'}")
    say(f"   에피소드: {desk['에피소드'] or '없음'}")
    facts = []
    say("② 도구 부르기")
    for name, args in plan["도구"]:
        key = name + json.dumps(args, ensure_ascii=False)       # 도구 + 값 = 이름표
        where = "캐시 적중" if key in cache else "그릇"
        if key not in cache:
            cache[key] = TOOLS[name](**args)
        facts.append(cache[key])
        say(f"   {name} ({where}) → {cache[key]}")
    desk["근거"] = "\n".join(facts)
    desk["단기"] = question
    used = [f"{k} {len(v)}/{BUDGET[k]}" for k, v in desk.items()]
    say("③ 작업대(토큰/예산): " + ", ".join(used))
    return desk

def check(answer, evidence):       # 답 속 숫자·조항·내선이 작업대 근거에 있나
    found = re.findall(r"\d+만 원|제\d+조|내선 \d+", answer)
    missing = [f for f in found if f not in evidence]
    return ("✓ 근거 있음" if not missing else f"✕ 근거 없음: {', '.join(missing)}")

if __name__ == "__main__":
    q = "10월 12일 부산 출장 식비 한도가 얼마였어요? 정산은 누구한테 물어봐요?"
    plan = {"좌표": [0.9, 0, 0, 0.4],                 # LLM이 질문을 나눈 계획의 예
            "도구": [("limit", {"item": "식비 한도", "date": "2026-10-12"}),
                     ("search_cards", {"qvec": [0.9, 0, 0, 0.4]}),
                     ("find_owner", {"rule": "국내 출장 규정"})]}
    print(f"━ 민지(1001): {q}")
    desk = run(1001, q, plan)
    good = ("10월 12일 출장이면 하루 3만 원이에요(국내 출장 규정 제2조). 11월부터는 "
            "4만 원입니다. 정산은 재무팀 준호 과장님(내선 2210)께 물어보세요.")
    bad = ("식비는 하루 5만 원이에요. "
           "정산은 재무팀 준호 과장님(내선 2210)께 물어보세요.")
    print("④ 답 검사: LLM이 쓴 답의 예", check(good, desk["근거"]))
    print("            지어낸 답의 예", check(bad, desk["근거"]))

    print("━ 서연(1003): 10월 12일 출장 식비 한도요?")
    run(1003, "10월 12일 출장 식비 한도요?",
        {"좌표": [0.9, 0, 0, 0.2],
         "도구": [("limit", {"item": "식비 한도", "date": "2026-10-12"})]})
