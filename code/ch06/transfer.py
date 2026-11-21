import sqlite3

db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE 예산 (부서명 TEXT PRIMARY KEY,
                   잔액 INTEGER NOT NULL CHECK (잔액 >= 0));   -- 단위: 만 원
INSERT INTO 예산 VALUES ('영업팀', 500), ('재무팀', 300);
""")

def balances():
    return dict(db.execute("SELECT 부서명, 잔액 FROM 예산 ORDER BY 부서명"))

def transfer(src, dst, amount, crash=False):
    try:
        with db:    # 블록을 무사히 마치면 commit, 오류가 나면 rollback
            db.execute("UPDATE 예산 SET 잔액 = 잔액 - ? WHERE 부서명 = ?", (amount, src))
            if crash:
                raise RuntimeError("두 번째 단계 전에 서버가 멈춤")
            db.execute("UPDATE 예산 SET 잔액 = 잔액 + ? WHERE 부서명 = ?", (amount, dst))
        print(f"✓ {amount}만 원 이체 완료  ", balances())
    except Exception as e:
        print(f"✕ {amount}만 원 이체 취소  ", balances(), f"← {e}")

print("처음                ", balances())
transfer("영업팀", "재무팀", 100)
transfer("영업팀", "재무팀", 100, crash=True)
transfer("영업팀", "재무팀", 900)

# 비교: 트랜잭션 없이(문장마다 바로 확정) 같은 사고가 나면?
db.isolation_level = None
db.execute("UPDATE 예산 SET 잔액 = 잔액 - 100 WHERE 부서명 = '영업팀'")  # 1단계 뒤 멈춤
print("트랜잭션 없이 멈추면  ", balances(), "← 100만 원이 사라짐")
