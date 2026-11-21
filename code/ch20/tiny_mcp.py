# 공부용 아주 작은 MCP: 표준 입출력(stdio)으로 JSON-RPC 메시지를 한 줄씩 주고받는다.
# 2026-07-28 명세의 일부만 따른다. 실제 서비스에서는 공식 SDK를 쓴다.
import json, subprocess, sys

VERSION = "2026-07-28"
M = "io.modelcontextprotocol/"                  # 명세가 정한 _meta 이름의 머리말

def schema(*need, optional=()):                 # 도구 입력의 모양 (JSON Schema)
    names = list(need) + list(optional)
    return {"type": "object", "properties": {n: {"type": "string"} for n in names},
            "required": list(need)}

def serve(name, tools):                         # tools = {이름: (설명, 모양, 함수)}
    sys.stdin.reconfigure(encoding="utf-8")     # 명세: 메시지는 UTF-8로 주고받는다
    sys.stdout.reconfigure(encoding="utf-8")
    for line in sys.stdin:                      # 서버: 한 줄 읽고, 한 줄 답한다
        req = json.loads(line)
        method, params = req["method"], req.get("params", {})
        version = params.get("_meta", {}).get(M + "protocolVersion")
        if version != VERSION:                  # 요청마다 버전을 확인한다
            out = {"error": {"code": -32022, "message": f"모르는 버전: {version}",
                             "data": {"supported": [VERSION], "requested": version}}}
        elif method == "server/discover":
            info = {"name": name, "version": "1.0"}
            out = {"result": {"supportedVersions": [VERSION],
                              "capabilities": {"tools": {}},
                              "_meta": {M + "serverInfo": info}}}
        elif method == "tools/list":
            out = {"result": {"tools": [
                {"name": n, "description": d, "inputSchema": s}
                for n, (d, s, f) in tools.items()]}}
        elif method == "tools/call" and params["name"] in tools:
            fn = tools[params["name"]][2]
            try:
                text, failed = fn(**params.get("arguments", {})), False
            except Exception as e:              # 도구가 실패해도 서버는 멈추지 않는다
                text, failed = f"도구 오류: {e}", True
            out = {"result": {"content": [{"type": "text", "text": text}],
                              "isError": failed}}
        elif method == "tools/call":
            out = {"error": {"code": -32602,
                             "message": f"Unknown tool: {params['name']}"}}
        else:
            out = {"error": {"code": -32601, "message": f"없는 메서드: {method}"}}
        if "result" in out:
            out["result"]["resultType"] = "complete"
        reply = {"jsonrpc": "2.0", "id": req["id"], **out}
        print(json.dumps(reply, ensure_ascii=False), flush=True)

class Client:                                   # 호스트 안의 클라이언트: 서버와 1:1
    def __init__(self, server_file, host="규정 도우미"):
        self.proc = subprocess.Popen([sys.executable, str(server_file)], text=True,
                                     encoding="utf-8", stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE)
        self.host, self.next_id = host, 0

    def request(self, method, **params):
        self.next_id += 1
        params["_meta"] = {M + "protocolVersion": VERSION,      # 요청마다 함께 보낸다
                           M + "clientCapabilities": {},
                           M + "clientInfo": {"name": self.host, "version": "1.0"}}
        msg = {"jsonrpc": "2.0", "id": self.next_id,
               "method": method, "params": params}
        self.proc.stdin.write(json.dumps(msg, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()
        return json.loads(self.proc.stdout.readline())

    def close(self):
        self.proc.stdin.close()
        self.proc.wait()
