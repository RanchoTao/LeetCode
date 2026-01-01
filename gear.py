t = int(input().strip())  # 读取测试用例数量

results = []
for _ in range(t):
    n = int(input().strip())  # 读取齿轮数量
    teeth = list(map(int, input().split()))  # 读取齿轮齿数列表
    
    # 核心逻辑：检查是否有重复齿数
    if len(teeth) != len(set(teeth)):
        results.append("YES")
    else:
        results.append("NO")

# 输出所有测试用例结果
for res in results:
    print(res)