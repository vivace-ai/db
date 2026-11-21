import math

# 영화마다 두 축의 좌표: (무거움 0~1, 상상 0~1). 실제 서비스라면 줄거리를 임베딩한 좌표
movies = {"우리 동네 빵집": (0.2, 0.1), "월요일의 반란": (0.1, 0.2),
          "마지막 편지":    (0.8, 0.1), "겨울 기차":     (0.7, 0.2),
          "달의 뒷면 탐험대": (0.3, 0.9), "용의 계곡":    (0.6, 0.8),
          "시간 도둑":      (0.8, 0.7)}

def nearest(point, k, skip=()):
    cands = [(round(math.dist(point, xy), 2), name) for name, xy in movies.items()
             if name not in skip]
    return sorted(cands)[:k]

print("이 영화를 좋아했다면:")
for name in ["우리 동네 빵집", "마지막 편지", "용의 계곡"]:
    near = nearest(movies[name], 1, skip={name})
    print(f"  {name} → {near[0][1]} (거리 {near[0][0]})")

liked = ["우리 동네 빵집", "달의 뒷면 탐험대"]          # 한 사람이 좋아한 두 영화
taste = tuple(round(sum(a) / len(liked), 2) for a in zip(*(movies[m] for m in liked)))
print(f"취향 좌표(두 영화의 평균): {taste}")
for d, name in nearest(taste, 3, skip=set(liked)):
    print(f"  추천 후보 → {name} (거리 {d})")
