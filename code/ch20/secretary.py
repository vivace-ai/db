import pathlib, sys
here = pathlib.Path(__file__).parent
sys.path.insert(0, str(here))
from tiny_mcp import Client

# 호스트(비서 앱) 하나에 서버 둘: 서버마다 클라이언트를 하나씩 만든다
servers = {"calendar": Client(here / "calendar_server.py", "업무 비서"),
           "mail": Client(here / "mail_server.py", "업무 비서")}
toolbox = [f"{s}.{t['name']}" for s, c in servers.items()
           for t in c.request("tools/list")["result"]["tools"]]
print("도구 상자:", ", ".join(toolbox[:2]))
print("          ", ", ".join(toolbox[2:]))

CONFIRM = {"calendar.add_event", "mail.send_mail"}   # 호스트가 정한 '사람에게 묻기'
answers = {"calendar.add_event": "예", "mail.send_mail": "아니요, 제가 읽고 보낼게요"}

# "다음 주 화요일 오후에 부산 거래처 미팅 잡고, 팀에 알릴 메일 써 줘"를 LLM이 나눈 예
plan = [("calendar.find_free_slots", {"date": "2026-11-24", "after": "13:00"}),
        ("calendar.add_event", {"date": "2026-11-24", "time": "13:00",
                                "title": "부산 거래처 미팅"}),
        ("mail.draft_mail", {"to": "영업팀", "subject": "11/24 부산 거래처 미팅",
                             "body": "화요일 13시에 부산 거래처와 미팅이 있습니다."}),
        ("mail.send_mail", {"draft_id": "d-1"})]   # 앞 결과에서 읽은 초안 번호
for full, args in plan:
    server, tool = full.split(".")
    if full in CONFIRM:                         # 바꾸거나 보내는 도구는 먼저 묻는다
        print(f"✋ {full} — 사람에게 확인: {answers[full]}")
        if answers[full] != "예":
            print("   → 부르지 않았다")
            continue
    else:
        print(f"· {full}")
    reply = servers[server].request("tools/call", name=tool, arguments=args)
    print("   →", reply["result"]["content"][0]["text"])
for c in servers.values():
    c.close()
