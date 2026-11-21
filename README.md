# AI 에이전트 데이터베이스 완전 정복 — 예제 코드

『AI 에이전트 데이터베이스 완전 정복』(김영희 지음, 완전 정복 시리즈)의 '직접 해 보기' 예제 코드입니다.

- **파이썬 3.9 이상만 있으면** 돌아갑니다. 데이터베이스 서버, API 키, 추가 라이브러리가 필요 없습니다.
- 책에 실린 '실행 결과'는 모두 이 코드를 그대로 돌려 나온 것입니다.
- 예제의 회사, 사람, 규정, 기사는 모두 지어낸 것입니다.

## 받기

- 이 페이지의 초록색 **Code** 단추 → **Download ZIP**을 누른 뒤 압축을 풉니다.
- 또는 `git clone https://github.com/vivace-ai/db.git`

## 실행하기

실행할 장의 폴더로 들어가 파일 이름을 입력합니다.

```text
cd code/ch05
python3 regdb.py          # Windows에서는 py regdb.py
```

- **순서가 있는 예제** — 5장의 `sql_five.py`는 `regdb.py`가 만든 `regdb.sqlite`를 씁니다. 책에 나온 순서대로 실행하세요.
- **함께 실행되는 파일** — 20장의 `agent_client.py`와 `secretary.py`는 같은 폴더의 서버 파일을 스스로 띄웁니다. 21장의 `agent.py`와 `evaluate.py`는 `stores.py`를 불러 씁니다.
- **Windows에서 한글이 깨지면** — `py -X utf8 파일이름.py`로 실행합니다.

자세한 준비 방법과 문제 해결은 책의 부록 C를 보세요.

## 장별 예제

| 장 | 제목 | 파일 |
|---|---|---|
| 1 | LLM은 기억하지 못한다 | `forgetful_bot.py` |
| 2 | 에이전트가 기억해야 할 다섯 가지 | `five_memories.py` |
| 3 | 데이터 그릇 지도 | `five_shapes.py` |
| 4 | 표로 생각하기 | `first_tables.py`, `library.py` |
| 5 | SQL 다섯 문장 | `regdb.py` → `sql_five.py` |
| 6 | 인덱스와 트랜잭션 | `index_plan.py`, `transfer.py`, `concert.py` |
| 7 | 에이전트가 SQL을 쓴다 | `schema_prompt.py`, `text2sql.py` |
| 8 | JSON 문서로 대화 기록 저장하기 | `json_basics.py`, `chat_store.py`, `shop_items.py` |
| 9 | 캐시로 자주 묻는 답 빠르게 꺼내기 | `postit_basics.py`, `postit_desk.py`, `weather_cache.py` |
| 10 | 임베딩: 문장을 좌표로 | `word_vs_meaning.py`, `movie_map.py` |
| 11 | 유사도: 거리와 각도 | `three_rulers.py`, `no_match.py`, `recipes.py` |
| 12 | 청킹과 메타데이터 | `chunker.py`, `metadata_filter.py`, `manual_cards.py` |
| 13 | 벡터 인덱스: 고속도로에서 골목길로 | `ivf.py`, `hnsw_toy.py`, `scale.py` |
| 14 | 벡터 데이터베이스 고르기 | `sqlite_vectors.py`, `choose_db.py` |
| 15 | 하이브리드 검색과 리랭킹 | `hybrid.py`, `shop_search.py` |
| 16 | 그래프 데이터베이스: 관계를 따라가는 기억 | `graph_rules.py`, `graph_in_sql.py`, `drama.py` |
| 17 | 온톨로지로 의미 구조화하기 | `ontology.py`, `infer.py`, `recipes.py` |
| 18 | GraphRAG: 그래프로 넓혀 찾기 | `extract.py`, `graphrag.py`, `news.py` |
| 19 | 단기·장기·에피소드 메모리 | `short_term.py`, `long_term.py`, `episodes.py`, `travel.py` |
| 20 | MCP로 데이터베이스 연결하기 | `tiny_mcp.py`, `regulation_server.py`, `agent_client.py`, `calendar_server.py`, `mail_server.py`, `secretary.py` |
| 21 | 완성: 사내 규정 도우미 에이전트 | `stores.py`, `agent.py`, `evaluate.py` |

파일은 책에 나오는 순서대로 적었습니다.

## 이 저장소에 없는 것

본문에서 '읽기만' 한 코드(Chroma, pgvector, 리랭커 모델, Neo4j Cypher, 공식 MCP SDK 등)는 별도 설치가 필요해 넣지 않았습니다. 책의 부록 C.7에 목록이 있습니다.

## 라이선스

예제 코드는 [MIT 라이선스](LICENSE)로 공개합니다. 출처를 밝히면 자유롭게 쓰고 고칠 수 있습니다. 책의 본문과 그림은 이 라이선스에 포함되지 않습니다.
