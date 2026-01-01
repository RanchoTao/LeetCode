import random
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 

def simulate_dice_even_frequency(n):
    even_count = 0
    frequencies = [] 
    
    for i in range(1, n + 1):
        roll = random.randint(1, 6)
        
        if roll % 2 == 0:
            even_count += 1
        
        current_frequency = even_count / i
        frequencies.append(current_frequency)
    
    return frequencies

def plot_frequency_chart(n=10000):
    print(f"开始模拟掷骰子{n}次...")
    frequencies = simulate_dice_even_frequency(n)
    
    plt.figure(figsize=(12, 8))
    
    plt.plot(range(1, n + 1), frequencies, linewidth=1, alpha=0.7, 
             label=f'偶数点数频率 (最终值: {frequencies[-1]:.4f})')
    
    theoretical_prob = 0.5
    plt.axhline(y=theoretical_prob, color='r', linestyle='--', 
                linewidth=2, label=f'理论概率 ({theoretical_prob})')
    
    plt.xlim(0, n)
    plt.ylim(0, 1)
    plt.xlabel('试验次数 (n)', fontsize=12)
    plt.ylabel('频率', fontsize=12)
    plt.title(f'掷骰子"点数为偶数"的频率变化 (n={n}次模拟)', fontsize=14)
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    
    stats_text = f"""最终统计:
总试验次数: {n}
偶数出现次数: {int(frequencies[-1] * n)}
最终频率: {frequencies[-1]:.4f}
与理论概率差值: {abs(frequencies[-1] - theoretical_prob):.4f}"""
    
    plt.annotate(stats_text, xy=(0.02, 0.98), xycoords='axes fraction',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.7),
                verticalalignment='top', fontsize=10)
    
    plt.tight_layout()
    plt.show()
    
    return frequencies

if __name__ == "__main__":
    n_simulations = 10000 
    
    frequencies = plot_frequency_chart(n_simulations)
    
    print(f"\n模拟结果摘要:")
    print(f"总试验次数: {n_simulations}")
    print(f"偶数点数最终频率: {frequencies[-1]:.4f}")
    print(f"理论概率: 0.5")
    print(f"绝对误差: {abs(frequencies[-1] - 0.5):.4f}")

def multiple_simulations(n_trials=10000, n_simulations=5):
    """多次模拟验证大数定律"""
    plt.figure(figsize=(12, 8))
    
    for i in range(n_simulations):
        frequencies = simulate_dice_even_frequency(n_trials)
        plt.plot(range(1, n_trials + 1), frequencies, linewidth=1, 
                alpha=0.7, label=f'模拟 {i+1} (最终: {frequencies[-1]:.4f})')
    
    plt.axhline(y=0.5, color='r', linestyle='--', linewidth=2, label='理论概率 (0.5)')
    plt.xlabel('试验次数')
    plt.ylabel('频率')
    plt.title(f'多次模拟验证: 掷骰子"点数为偶数"的频率变化', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

multiple_simulations(n_trials=5000, n_simulations=5)