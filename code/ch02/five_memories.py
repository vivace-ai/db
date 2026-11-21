# 사실 기억: 공식 규정 (출처와 시행일을 함께 저장)
facts = {
    "국내출장_식비": {"내용": "하루 4만 원", "출처": "국내 출장 규정 제2조",
                     "시행일": "2026-11-01"},
    "연차_기본": {"내용": "1년 근무 시 15일", "출처": "취업 규칙 제4조",
                 "시행일": "2025-01-01"},
}
# 경험 기억: 지난 대화에서 남긴 메모
episodes = [{"사용자": "민지", "날짜": "2026-11-13",
             "메모": "답을 표로 받는 것을 좋아함"}]
# 절차 기억: 일하는 규칙
procedures = ["답에는 반드시 규정 출처를 붙인다.",
              "규정에 없는 내용은 추측하지 말고 담당 부서를 안내한다."]
# 대화 기억: 이번 대화
session = [{"role": "user", "content": "다음 주에 부산 출장 가요."},
           {"role": "assistant", "content": "국내 출장이시군요. 무엇이 궁금하세요?"}]

def build_workbench(user, question, budget=300):
    """작업 기억(작업대)을 조립한다: 네 가지 기억에서 필요한 것만 골라 예산 안에서"""
    hits = [f'{v["내용"]} ({v["출처"]})' for k, v in facts.items()
            if any(w in k for w in question.split())]
    memos = [e["메모"] for e in episodes if e["사용자"] == user]
    parts = [
        "[일하는 규칙] " + "\n  ".join(procedures),
        "[이 사용자] " + " ".join(memos),
        "[찾은 규정] " + (" / ".join(hits) or "없음"),
        "[최근 대화] " + " → ".join(m["content"] for m in session[-2:]),
        "[질문] " + question,
    ]
    text = "\n".join(parts)
    print(f"작업대 사용량: {len(text)}자 / 예산 {budget}자\n")
    if len(text) > budget:
        print("⚠ 예산 초과: 대화나 자료를 줄여야 합니다\n")
    return text

print(build_workbench("민지", "국내 식비 한도는?"))
