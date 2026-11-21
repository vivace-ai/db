import sqlite3, pathlib

DB = pathlib.Path(__file__).with_name("concert.sqlite")
DB.unlink(missing_ok=True)
setup = sqlite3.connect(DB)
# 예매자가 비면 빈 좌석
setup.execute("CREATE TABLE 좌석 (좌석번호 TEXT PRIMARY KEY, 예매자 TEXT)")
setup.executemany("INSERT INTO 좌석 VALUES (?, NULL)", [("A-12",), ("A-13",)])
setup.commit()
setup.close()

하늘 = sqlite3.connect(DB, isolation_level=None)      # 두 사람의 휴대폰 = 두 개의 연결
바다 = sqlite3.connect(DB, isolation_level=None)

def owner(db, seat):
    return db.execute("SELECT 예매자 FROM 좌석 WHERE 좌석번호 = ?", (seat,)).fetchone()[0]

print("① 읽고 나서 쓰기")
for name, db in [("하늘", 하늘), ("바다", 바다)]:      # 두 사람이 거의 동시에 좌석을 본다
    print(f"  {name} 님이 본 A-12: {owner(db, 'A-12') or '빈 좌석'}")
for name, db in [("하늘", 하늘), ("바다", 바다)]:      # 둘 다 비었다고 믿고 자기 이름을 쓴다
    db.execute("UPDATE 좌석 SET 예매자 = ? WHERE 좌석번호 = 'A-12'", (name,))
    print(f"  {name} 님: 예매 완료!")
print(f"  실제 A-12 주인: {owner(하늘, 'A-12')} → 하늘 님의 표는 허공에")

def book(db, name, seat):                            # 확인과 쓰기를 한 문장으로
    cur = db.execute("UPDATE 좌석 SET 예매자 = ? WHERE 좌석번호 = ? AND 예매자 IS NULL",
                     (name, seat))
    return "예매 완료!" if cur.rowcount == 1 else "이미 팔린 좌석입니다"

print("② 비어 있을 때만 쓰기")
print(f"  하늘 님: {book(하늘, '하늘', 'A-13')}")
print(f"  바다 님: {book(바다, '바다', 'A-13')}")
print(f"  실제 A-13 주인: {owner(바다, 'A-13')}")
