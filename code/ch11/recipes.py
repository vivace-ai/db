import math

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))

# 재료 무게(g): (돼지고기, 김치, 두부, 대파, 된장)
recipes = {"김치찌개 2인분": (150, 200, 150, 30, 0),
           "김치찌개 4인분": (300, 400, 300, 60, 0),
           "된장찌개 2인분": (50, 0, 150, 30, 40),
           "제육볶음 2인분": (300, 0, 0, 50, 0)}
fridge = (100, 150, 50, 0, 0)                      # 냉장고에 남은 재료

a, b = recipes["김치찌개 2인분"], recipes["김치찌개 4인분"]
print(f"김치찌개 2인분 ↔ 4인분: 거리 {math.dist(a, b):.0f}, 코사인 {cosine(a, b):.2f}")
by_cos = sorted(recipes, key=lambda n: cosine(fridge, recipes[n]), reverse=True)
by_dist = sorted(recipes, key=lambda n: math.dist(fridge, recipes[n]))
print("냉장고 재료와 비교 (코사인 순서대로)")
for name in by_cos:
    r = recipes[name]
    print(f"  {name}: 코사인 {cosine(fridge, r):.2f} {by_cos.index(name) + 1}등"
          f" · 거리 {math.dist(fridge, r):3.0f} {by_dist.index(name) + 1}등")
