# 규정 도우미의 서고: 책에서 만든 그릇들을 한자리에 (모두 메모리 안의 작은 판)
import math, sqlite3

# 관계형 DB (2부): 시행일과 종료일이 있는 규정 조항
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE 규정조항 (규정 TEXT, 조항 TEXT, 항목 TEXT, 값 TEXT,
                       시행일 TEXT, 종료일 TEXT);
INSERT INTO 규정조항 VALUES
 ('국내 출장 규정', '제2조', '식비 한도', '하루 3만 원', '2025-01-01', '2026-10-31'),
 ('국내 출장 규정', '제2조', '식비 한도', '하루 4만 원', '2026-11-01', NULL),
 ('국내 출장 규정', '제3조', '숙박비 한도', '하루 7만 원', '2025-01-01', NULL);""")

# 벡터 DB (4부): 규정 카드와 좌표 (축: 돈·식비, 잠·숙박, 잃어버림, 사람·담당)
cards = {"제2조 식비": ("제2조(식비) 출장자에게 하루 4만 원까지 식비를 지급한다.",
                      (0.9, 0.1, 0, 0)),
         "제3조 숙박비": ("제3조(숙박비) 숙박비는 하루 7만 원까지 지급한다.",
                        (0.3, 0.9, 0, 0)),
         "제6조 분실": ("제6조(분실) 영수증을 잃어버린 경우 사유서를 내면 지급한다.",
                      (0.2, 0, 0.9, 0.1))}

# 그래프 (5부): 규정 → 담당 부서 → 팀장
edges = [("국내 출장 규정", "담당", "재무팀"),
         ("재무팀", "팀장", "준호 과장(내선 2210)")]

# 기억 (19장): 사람에 대한 장기 기억과 공용 에피소드
long_term = {1001: {"답 형식": "짧은 문장 두세 줄"}}
episodes = [("정산 질문에는 출장 날짜를 먼저 확인한다", (0.9, 0, 0, 0.3)),
            ("영수증 분실에는 사유서 양식 위치까지 알려 준다", (0.2, 0, 0.9, 0.1))]

def cos(a, b):
    return sum(x * y for x, y in zip(a, b)) / (math.hypot(*a) * math.hypot(*b))

# 도구 (7장의 정해 둔 도구, 20장이라면 MCP 서버가 내놓을 것들)
def limit(item, date):
    row = db.execute("SELECT 값, 규정, 조항 FROM 규정조항 WHERE 항목 = ? "
                     "AND 시행일 <= ? AND (종료일 IS NULL OR 종료일 >= ?)",
                     (item, date, date)).fetchone()          # 5장의 시점 조건
    return f"{date} 기준 {item}: {row[0]} ({row[1]} {row[2]})"

def search_cards(qvec, k=1):
    best = sorted(cards.values(), key=lambda c: cos(qvec, c[1]), reverse=True)[:k]
    return " / ".join(text for text, _ in best)

def find_owner(rule):
    dept = next(b for a, r, b in edges if a == rule and r == "담당")
    boss = next(b for a, r, b in edges if a == dept and r == "팀장")
    return f"{rule} 담당: {dept}, 팀장 {boss}"

TOOLS = {"limit": limit, "search_cards": search_cards, "find_owner": find_owner}
