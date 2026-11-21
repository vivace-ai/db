import random

LLM_SEC, NOTE_SEC = 2.0, 0.001          # 한 번 답하는 데 걸리는 시간(가정)
asked = [                               # 직원들이 실제로 입력한 모양들
    "연차 며칠이에요?", "연차 며칠이에요", "연차  며칠이에요 ?", "연차는 며칠인가요?",
    "식비 한도가 얼마예요?", "식비 한도가 얼마예요", "식비 한도는 얼마인가요?",
    "숙박비 한도가 얼마예요?"]
random.seed(9)
day = random.choices(asked, weights=[30, 12, 6, 8, 18, 8, 6, 12], k=100)   # 하루 100번

def slow_answer(question):              # 느린 길: 서고를 뒤지고 LLM이 답을 쓴다
    return f"({question}에 대한 답)"

def key_as_typed(q):                    # 이름표 ①: 입력한 글자 그대로
    return q

def key_trimmed(q):                     # 이름표 ②: 띄어쓰기·물음표를 지운 글자
    return "".join(ch for ch in q if ch.isalnum())

def run(make_key):
    notes, hit, miss = {}, 0, 0         # notes = 책상 위 포스트잇 (이름표 → 답)
    for q in day:
        key = make_key(q)
        if key in notes:
            hit += 1                    # 적중: 포스트잇에서 바로 답한다
        else:
            miss += 1                   # 실패: 느린 길로 가서 답을 받고
            notes[key] = slow_answer(q) #       포스트잇에 적어 둔다
    return hit, miss, len(notes), miss * LLM_SEC + hit * NOTE_SEC

print(f"캐시 없음       : 느린 길 100번, 약 {100 * LLM_SEC:.0f}초")
for name, make_key in [("이름표 ① 그대로", key_as_typed), ("이름표 ② 다듬기", key_trimmed)]:
    hit, miss, n, sec = run(make_key)
    print(f"{name}: 느린 길 {miss}번, 약 {sec:.0f}초, "
          f"적중률 {hit / len(day):.0%}, 포스트잇 {n}장")
print(key_trimmed("연차  며칠이에요 ?"), "/", key_trimmed("연차는 며칠인가요?"))
