def choose(cards, has_postgres, has_ops_team):
    """세 가지 질문으로 고르는 출발점 (숫자는 대략적인 눈금)"""
    if cards <= 100_000 and not has_postgres:
        return "내장형(SQLite·Chroma)", "카드가 적다. 서버 없이 파일 하나로"
    if has_postgres and cards <= 10_000_000:
        return "pgvector", "쓰던 PostgreSQL에 벡터 칸을 더한다"
    if not has_ops_team:
        return "관리형 서비스", "돌볼 사람이 없다. 운영을 맡긴다"
    return "전용 벡터 DB(Qdrant·Milvus 등)", "규모가 크다. 여러 서버를 직접 조정"

services = [("규정 도우미 첫 버전", 1_000, False, False),
            ("사내 문서 검색", 2_000_000, True, True),
            ("쇼핑몰 상품 추천", 50_000_000, True, True),
            ("사진 앱 비슷한 사진 찾기", 100_000_000, False, False)]
for name, cards, pg, ops in services:
    pick, why = choose(cards, pg, ops)
    print(f"{name} ({cards:,}장)")
    print(f"  → {pick}: {why}")
