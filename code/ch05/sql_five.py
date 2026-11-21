import sqlite3, pathlib

DB = pathlib.Path(__file__).with_name("regdb.sqlite")   # regdb.py가 만든 파일
if not DB.exists():
    raise SystemExit("regdb.sqlite가 없습니다. regdb.py를 먼저 실행하세요.")
db = sqlite3.connect(DB)
db.execute("PRAGMA foreign_keys = ON")

def show(title, sql, params=()):
    print(f"▶ {title}")
    for row in db.execute(sql, params):
        print("  ", row)

# ① SELECT: 고르고, 거르고, 정렬한다
show("영업팀 직원", "SELECT 직원번호, 이름, 직급 FROM 직원 "
                    "WHERE 부서번호 = ? ORDER BY 직원번호", (10,))

# ② INSERT · ③ UPDATE: 넣고 고친다 (UPDATE에는 반드시 WHERE)
db.execute("INSERT INTO 직원 (직원번호, 이름, 직급, 부서번호) VALUES (?, ?, ?, ?)",
           (1006, "지수", "사원", 10))
db.execute("UPDATE 직원 SET 직급 = ? WHERE 직원번호 = ?", ("대리", 1003))
show("넣고 고친 뒤 영업팀", "SELECT 직원번호, 이름, 직급 FROM 직원 "
                           "WHERE 부서번호 = 10 ORDER BY 직원번호")

# ④ DELETE: 지운다 (DELETE에도 반드시 WHERE)
db.execute("DELETE FROM 직원 WHERE 직원번호 = ?", (1006,))

# ⑤ JOIN: 표를 다시 잇는다 (LEFT JOIN은 짝이 없는 부서도 남긴다)
show("부서별 인원", "SELECT 부서.부서명, COUNT(직원.직원번호) FROM 부서 "
                    "LEFT JOIN 직원 ON 직원.부서번호 = 부서.부서번호 "
                    "GROUP BY 부서.부서번호 ORDER BY 부서.부서번호")

# 덤: 출장 날짜에 유효한 식비 한도 찾기 (2장의 약속)
for day in ["2026-10-12", "2026-11-20"]:
    show(f"{day} 출장의 식비 한도",
         "SELECT 값, 시행일 FROM 규정조항 WHERE 항목 = '식비 한도' "
         "AND 시행일 <= ? AND (종료일 IS NULL OR 종료일 >= ?)", (day, day))

db.rollback()          # 연습으로 바꾼 내용은 되돌려 파일을 처음 상태로 둔다
