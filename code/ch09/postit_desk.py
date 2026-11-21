from collections import OrderedDict
from datetime import datetime, timedelta

class PostIt:                                   # 책상 위 포스트잇 묶음
    def __init__(self, size, ttl):
        self.notes = OrderedDict()              # 이름표 → (답, 떼어 낼 시각)
        self.size, self.ttl = size, ttl

    def get(self, key, now):
        if key not in self.notes:
            return None, "실패"
        answer, expire = self.notes[key]
        if now >= expire:                       # 수명이 다했다 → 떼고 실패로
            del self.notes[key]
            return None, "실패(만료)"
        self.notes.move_to_end(key)             # 방금 본 것은 맨 위로
        return answer, "적중"

    def put(self, key, answer, now):
        self.notes[key] = (answer, now + self.ttl)
        self.notes.move_to_end(key)
        if len(self.notes) > self.size:         # 자리가 없으면
            return self.notes.popitem(last=False)[0]   # 가장 오래 안 본 것을 뗀다

    def drop(self, key):                        # 정본이 바뀌었을 때 바로 뗀다
        self.notes.pop(key, None)

def scenario(title, fix):
    print(title)
    shelf = {"식비": "하루 3만 원", "숙박비": "하루 7만 원", "연차": "1년 근무 시 15일"}
    desk = PostIt(size=2, ttl=timedelta(days=7))

    def ask(topic, when):
        now = datetime.strptime("2026-" + when, "%Y-%m-%d %H:%M")
        answer, tag = desk.get(topic, now)
        if answer is None:                      # 실패하면 서고(정본)에서 읽고 붙인다
            answer = shelf[topic]
            gone = desk.put(topic, answer, now)
            tag += " → 서고" + (f" ('{gone}' 포스트잇을 뗌)" if gone else "")
        warn = "  ✗ 서고와 다른 낡은 답" if answer != shelf[topic] else ""
        print(f"  [{when}] {topic}? {tag} → {answer}{warn}")

    ask("식비", "10-31 09:00")
    ask("식비", "10-31 13:00")
    print("  ~ 11-01 0시, 식비 한도가 하루 4만 원으로 바뀜")
    shelf["식비"] = "하루 4만 원"
    if fix:
        desk.drop("식비")                       # 정본을 고치는 곳에서 포스트잇도 뗀다
    ask("식비", "11-02 09:00")
    return ask

ask = scenario("① 서고만 고쳤을 때", fix=False)
ask("식비", "11-07 09:00")                      # 붙인 지 7일, 수명이 다했다
ask = scenario("② 서고를 고치면서 포스트잇도 뗐을 때 (자리는 두 장)", fix=True)
ask("숙박비", "11-02 09:10")
ask("식비", "11-02 09:20")
ask("연차", "11-02 09:30")
