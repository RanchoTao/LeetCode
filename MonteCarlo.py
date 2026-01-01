import random

def estimate_pi(num_samples):
    inside_circle = 0

    for _ in range(num_samples):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        if x**2 + y**2 <= 1:
            inside_circle += 1

    pi_estimate = (inside_circle / num_samples) * 4
    return pi_estimate

# 示例：使用 1,000,000 个样本点估算 π
samples = 1000000
pi = estimate_pi(samples)
print(f"使用 {samples} 个样本估算的 π 值为：{pi}")