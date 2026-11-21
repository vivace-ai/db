# 장기 기억: 이 사람에 대해 알고 있는 것 (선호)
prefs = {"출발 시각": "오전 7시 전 출발은 싫다", "숙소": "바다가 보이는 곳"}
# 에피소드 기억: 지난 여행에서 겪은 일과 교훈 (주제별로 꺼내 쓴다)
lessons = {"렌터카": ("2025-07 제주", "사흘 전에 예약했더니 성수기라 두 배 값"),
           "숙소": ("2026-03 오사카", "역에서 멀어 날마다 택시를 탔다")}
# 단기 기억: 이번 대화에서 들은 것
request = {"곳": "강릉", "기간": "연말 2박 3일", "필요": ["기차", "숙소", "렌터카"]}

trains = ["06:05", "08:10", "10:30"]                     # 서울역 → 강릉
# 숙소 후보: (이름, 바다가 보이나, 역까지 걸어서 몇 분)
hotels = [("솔바람 호텔", True, 8), ("파도 리조트", True, 25),
          ("강릉역 비즈니스호텔", False, 3)]

print(f"요청(단기): {request['곳']} {request['기간']}, {'·'.join(request['필요'])}")
for t in trains:
    if t < "07:00":
        print(f"  ✕ 기차 {t}  ← 장기 기억: {prefs['출발 시각']}")
    else:
        print(f"  ✓ 기차 {t} 서울역 → 강릉")
        break
for name, sea, walk in hotels:
    if not sea:
        print(f"  ✕ {name}  ← 장기 기억: {prefs['숙소']}")
    elif walk > 10:
        print(f"  ✕ {name} (역에서 {walk}분)  ← 에피소드: {lessons['숙소'][0]}")
    else:
        print(f"  ✓ {name} (바다 보임, 역에서 걸어서 {walk}분)")
if "렌터카" in request["필요"] and "렌터카" in lessons:
    when, what = lessons["렌터카"]
    print(f"  ! 렌터카는 지금 예약하세요  ← 에피소드: {when}")
    print(f"    ({what})")
