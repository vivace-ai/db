# 일정 서버: 빈 시간 찾기(읽기), 일정 넣기(쓰기)
from tiny_mcp import schema, serve

events = {"2026-11-24": {"09:00": "팀 회의", "11:00": "보고서 검토", "15:00": "면담"}}
HOURS = ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00", "17:00"]

def find_free_slots(date, after="09:00"):
    busy = events.get(date, {})
    free = [h for h in HOURS if h >= after and h not in busy]
    return f"{date} 빈 시간: " + ", ".join(free)

def add_event(date, time, title):
    events.setdefault(date, {})[time] = title
    return f"일정을 넣었다: {date} {time} {title}"

serve("calendar", {
    "find_free_slots": ("날짜의 빈 시간을 찾는다. after로 시작 시각을 정한다.",
                        schema("date", optional=["after"]), find_free_slots),
    "add_event": ("일정을 하나 넣는다. 사용자의 일정표가 바뀐다.",
                  schema("date", "time", "title"), add_event)})
