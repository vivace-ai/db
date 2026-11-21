import random

random.seed(7)
asks = sorted(random.sample(range(24 * 60), 300))   # 하루(1440분) 동안 질문 300번이 온 시각

def weather_api(minute):            # 가짜 날씨 API: 날씨는 정각마다 바뀐다고 가정
    return f"{minute // 60}시 날씨"

def simulate(ttl):                  # ttl: 포스트잇 수명(분), None이면 '다음 정각까지'
    note, expire = None, -1
    calls = stale = 0
    for t in asks:
        if t >= expire:             # 없거나 수명이 다했으면 API를 부른다
            note = weather_api(t)
            expire = t + ttl if ttl else (t // 60 + 1) * 60
            calls += 1
        if note != weather_api(t):  # 포스트잇의 답이 지금 날씨와 다르면 낡은 답
            stale += 1
    return calls, stale

for ttl in [1, 10, 30, 60, 360, None]:
    calls, stale = simulate(ttl)
    name = f"수명 {ttl}분" if ttl else "다음 정각까지"
    rate = f"{stale / len(asks):.0%}"
    print(f"API 호출 {calls:>3}번, 낡은 답 {stale:>3}번 ({rate:>3}) ← {name}")
