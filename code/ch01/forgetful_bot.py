def llm(messages):
    """진짜 LLM 대신, 받은 메시지만 보고 답하는 흉내 함수"""
    last = messages[-1]["content"]
    seen = " ".join(m["content"] for m in messages)   # 작업대에 올라온 글 전체
    if "이름이 뭐" in last:
        return "민지 님이시죠!" if "민지" in seen else "죄송해요, 처음 뵙는 것 같아요."
    return "네, 기억해 둘게요."

# ① 매번 새 대화로 부르면
print(llm([{"role": "user", "content": "제 이름은 민지예요."}]))
print(llm([{"role": "user", "content": "제 이름이 뭐였죠?"}]))

# ② 이전 대화를 함께 올려 주면
history = [{"role": "user", "content": "제 이름은 민지예요."}]
history.append({"role": "assistant", "content": llm(history)})
history.append({"role": "user", "content": "제 이름이 뭐였죠?"})
print(llm(history))
