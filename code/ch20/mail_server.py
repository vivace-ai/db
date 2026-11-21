# 메일 서버: 초안 쓰기(보관만), 보내기(되돌릴 수 없음)
from tiny_mcp import schema, serve

drafts = {}

def draft_mail(to, subject, body):
    draft_id = f"d-{len(drafts) + 1}"
    drafts[draft_id] = (to, subject, body)
    return f"초안 {draft_id}을 보관했다: [{subject}] 받는 사람 {to}"

def send_mail(draft_id):
    to, subject, _ = drafts.pop(draft_id)
    return f"{to}에게 메일을 보냈다: [{subject}]"

serve("mail", {
    "draft_mail": ("메일 초안을 써서 보관한다. 보내지는 않는다.",
                   schema("to", "subject", "body"), draft_mail),
    "send_mail": ("보관한 초안을 보낸다. 보낸 메일은 되돌릴 수 없다.",
                  schema("draft_id"), send_mail)})
