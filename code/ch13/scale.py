# 카드 수에 따라 벡터를 저장하는 데 드는 메모리 (숫자 하나 = 4바이트, float32)
DIM = 768                                    # 10장의 한국어 모델과 같은 차원

def size(n, bytes_per_number):
    gb = n * DIM * bytes_per_number / 1e9
    return f"{gb:,.1f}GB" if gb >= 1 else f"{gb * 1000:,.1f}MB"

print("카드 수         float32(4바이트)  int8(1바이트)")
for n, what in [(1_000, "규정 도우미"), (1_000_000, "회사 전체 문서"),
                (100_000_000, "사진·음악 서비스")]:
    print(f"{n:>11,}장  {size(n, 4):>12}  {size(n, 1):>12}   ← {what}")
