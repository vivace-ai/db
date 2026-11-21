facts = {("재무팀", "상위", "경영지원본부"), ("인사팀", "상위", "경영지원본부"),
         ("경영지원본부", "상위", "회사"), ("영업팀", "상위", "회사"),
         ("재무팀", "팀장", "준호"), ("민지(1005)", "소속", "재무팀"),
         ("도윤", "소속", "인사팀")}

def infer(facts):                        # 규칙을 더 나올 것이 없을 때까지 적용한다
    facts = set(facts)
    while True:
        new = set()
        for a, r1, b in facts:
            for c, r2, d in facts:
                if r1 == r2 == "상위" and b == c:          # 규칙 ①: 상위의 상위도 상위
                    new.add((a, "상위", d))
                # 규칙 ②: 소속 부서의 상위에도 소속
                if r1 == "소속" and r2 == "상위" and b == c:
                    new.add((a, "소속", d))
            if r1 == "팀장":                    # 규칙 ③: 팀장은 그 부서 소속
                new.add((b, "소속", a))
        if new <= facts:
            return facts
        facts |= new

all_facts = infer(facts)
print(f"적어 둔 사실 {len(facts)}개 → 추론까지 {len(all_facts)}개")
for who in sorted({a for a, r, b in all_facts if r == "소속" and b == "경영지원본부"}):
    how = "적어 둠" if (who, "소속", "경영지원본부") in facts else "추론"
    print(f"  경영지원본부 소속: {who} ({how})")
print("준호의 소속:", sorted(b for a, r, b in all_facts if a == "준호" and r == "소속"))
