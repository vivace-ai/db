import re, textwrap

doc = ("제1조(목적) 이 규정은 국내 출장 비용의 지급 기준을 정한다. "
       "제2조(식비) 출장자에게 하루 4만 원까지 식비를 지급한다. 영수증을 내야 한다. "
       "제3조(숙박비) 숙박비는 하루 7만 원까지 지급한다. "
       "다만 회사가 숙소를 제공하면 지급하지 않는다.")

def fixed(text, size, overlap=0):           # ① 글자 수로 자르기 (겹치기 가능)
    step = size - overlap
    return [text[i:i + size] for i in range(0, len(text) - overlap, step)]

def by_article(text):                       # ② 조항 단위로 자르기
    return [c.strip() for c in re.split(r"(?=제\d+조)", text) if c.strip()]

print(f"규정 전체 {len(doc)}자")
print("① 30자씩 자르기")
for i, c in enumerate(fixed(doc, 30)):
    print(f"  [{i}] {c}")
print("② 30자씩, 8자 겹치기")
for i, c in enumerate(fixed(doc, 30, 8)[1:3], start=1):
    print(f"  [{i}] {c}")
print("③ 조항 단위 + 머리말")
for c in by_article(doc):                   # 긴 카드는 출력할 때만 줄을 나눈다
    print(textwrap.fill(f"[국내 출장 규정] {c}", 60,
                        initial_indent="  ", subsequent_indent="    "))
