# 이번 대화 (2장 2.4절의 대화 기억 = 단기 기억)
talk = [("user", "다음 주 화요일부터 1박 2일로 부산 출장 가요."),
        ("assistant", "국내 출장이시군요. 무엇이 궁금하세요?"),
        ("user", "KTX를 타려는데 교통비는 실비로 받나요?"),
        ("assistant", "네, 제8조에 따라 실제 낸 요금을 정산합니다. "
                      "영수증을 챙기세요."),
        ("user", "숙소는 해운대 쪽 호텔로 잡으려고요."),
        ("assistant", "숙박비는 하루 7만 원까지입니다(제3조)."),
        ("user", "식비는요?")]

BUDGET = 100                                  # 대화 기억에 내준 작업대 자리 (토큰)

def tokens(msgs):                             # 한 글자를 1토큰으로 어림한다
    return sum(len(text) for _, text in msgs)

# 오래된 메시지를 LLM에게 요약해 달라고 하면 돌아올 법한 답의 예
summary = ("system", "앞선 대화 요약: 다음 주 화요일부터 1박 2일 부산 출장. "
                     "교통비는 실비(제8조) 안내. 숙소는 해운대 쪽 호텔.")

def fold(msgs, keep):                         # 예산을 넘으면 오래된 것을 요약으로
    if tokens(msgs) <= BUDGET:
        return msgs
    return [summary] + msgs[-keep:]

for name, desk in [("① 전부 올리기", talk), ("② 최근 2개만", talk[-2:]),
                   ("③ 요약 + 최근 2개", fold(talk, 2))]:
    over = "예산 초과 ✕" if tokens(desk) > BUDGET else "예산 안 ✓"
    days = "✓" if any("1박 2일" in text for _, text in desk) else "✕"
    print(f"{name}: 메시지 {len(desk)}개, {tokens(desk)}토큰 ({over})")
    print(f"   '1박 2일'이 작업대에 있나? {days}")
