import json, pathlib, sys
here = pathlib.Path(__file__).parent
sys.path.insert(0, str(here))                   # 같은 폴더의 tiny_mcp.py를 불러오려고
from tiny_mcp import Client, M

server = Client(here / "regulation_server.py")  # 서버를 따로 띄우고 연결한다

info = server.request("server/discover")["result"]
print("① 서버 알아보기:", info["_meta"][M + "serverInfo"]["name"],
      "· 버전", info["supportedVersions"])

print("② 도구 목록 (LLM의 작업대에 올라갈 설명서)")
for tool in server.request("tools/list")["result"]["tools"]:
    print(f"   {tool['name']}: {tool['description']}")

print("③ 도구 부르기 (LLM이 고른 호출의 예)")
for name, args in [("search_rules", {"keyword": "식비"}),
                   ("get_article", {"rule": "국내 출장 규정", "number": "제12조"}),
                   ("delete_rule", {"number": "제2조"})]:
    print(f"   {name} {json.dumps(args, ensure_ascii=False)}")
    reply = server.request("tools/call", name=name, arguments=args)
    if "error" in reply:                        # 프로토콜 오류: 요청 자체가 잘못됨
        print(f"   → 오류 {reply['error']['code']}: {reply['error']['message']}")
    else:                                       # 도구 결과: 실패해도 결과로 돌아온다
        mark = "isError" if reply["result"]["isError"] else "결과"
        print(f"   → {mark}: {reply['result']['content'][0]['text']}")
server.close()
