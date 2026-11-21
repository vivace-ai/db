import json

msg = {"role": "assistant", "content": "하루 4만 원입니다.",
       "근거": {"규정": "국내 출장 규정", "조항번호": 2}}

text = json.dumps(msg, ensure_ascii=False, indent=2)   # 파이썬 값 → JSON 글자
print(text)

back = json.loads(text)                          # JSON 글자 → 파이썬 값
print(type(back).__name__, type(back["근거"]).__name__, back["근거"]["조항번호"])
print(json.dumps({"확인됨": True, "점수": None}, ensure_ascii=False))
print(json.dumps({"규정": "출장"}))              # ensure_ascii를 빼면?
