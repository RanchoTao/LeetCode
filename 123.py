import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class FastDiceProbability:
    def __init__(self, max_trials=1000, speed_mode='fast'):
        """
        初始化快速骰子概率模拟
        
        参数:
        max_trials: 最大试验次数
        speed_mode: 速度模式 ('slow', 'normal', 'fast', 'ultra_fast')
        """
        self.max_trials = max_trials
        self.speed_mode = speed_mode
        
        # 根据速度模式设置参数
        self.speed_params = {
            'slow': {'interval': 500, 'batch_size': 1, 'update_interval': 1},
            'normal': {'interval': 200, 'batch_size': 1, 'update_interval': 1},
            'fast': {'interval': 50, 'batch_size': 5, 'update_interval': 1},
            'ultra_fast': {'interval': 10, 'batch_size': 20, 'update_interval': 5}
        }
        
        params = self.speed_params[speed_mode]
        self.batch_size = params['batch_size']
        self.update_interval = params['update_interval']
        
        # 数据存储
        self.trials = []
        self.frequencies = []
        self.even_count = 0
        self.total_count = 0
        
        # 创建画布和子图
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 10))
        self.fig.suptitle(f'🎲 骰子偶数点数概率动态模拟 ({speed_mode.upper()} MODE)', 
                         fontsize=16, fontweight='bold')
        
        # 设置频率曲线图
        self.ax1.set_xlim(0, max_trials)
        self.ax1.set_ylim(0, 1)
        self.ax1.set_xlabel('试验次数 (n)')
        self.ax1.set_ylabel('频率')
        self.ax1.set_title('偶数点数频率随试验次数的变化')
        self.ax1.grid(True, alpha=0.3)
        
        # 理论概率线
        self.theoretical_line = self.ax1.axhline(y=0.5, color='red', linestyle='--', 
                                               linewidth=2, label='理论概率 (0.5)')
        # 频率曲线
        self.frequency_line, = self.ax1.plot([], [], 'b-', linewidth=1.5, 
                                            label='实际频率', alpha=0.8)
        
        # 实时数据显示
        self.current_freq_text = self.ax1.text(0.02, 0.95, '', transform=self.ax1.transAxes,
                                              bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.8),
                                              fontsize=10)
        
        self.ax1.legend(loc='lower right')
        
        # 设置当前骰子结果显示
        self.ax2.set_xlim(0, 10)
        self.ax2.set_ylim(0, 10)
        self.ax2.set_title('当前骰子结果')
        self.ax2.axis('off')  # 隐藏坐标轴
        
        # 骰子显示文本
        self.dice_text = self.ax2.text(5, 7, '等待开始...', ha='center', va='center', 
                                      fontsize=40, color='blue', fontweight='bold')
        
        # 结果统计文本
        self.stats_text = self.ax2.text(5, 3, '', ha='center', va='center',
                                       fontsize=12, bbox=dict(boxstyle="round,pad=0.5", facecolor="lightblue", alpha=0.7))
        
        # 动画控制
        self.is_paused = False
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        
    def on_click(self, event):
        """点击暂停/继续动画"""
        if event.inaxes == self.ax1 or event.inaxes == self.ax2:
            self.is_paused = not self.is_paused
            status = "暂停" if self.is_paused else "继续"
            print(f"动画已{status}")
    
    def simulate_dice_roll(self):
        """模拟一次骰子投掷并返回结果"""
        roll = random.randint(1, 6)
        is_even = (roll % 2 == 0)
        return roll, is_even
    
    def update_frequency_batch(self):
        """批量更新频率数据"""
        batch_results = []
        for _ in range(self.batch_size):
            if self.total_count >= self.max_trials:
                break
                
            roll, is_even = self.simulate_dice_roll()
            self.total_count += 1
            if is_even:
                self.even_count += 1
            
            batch_results.append((roll, is_even))
        
        if self.total_count > 0:
            current_frequency = self.even_count / self.total_count
            self.trials.append(self.total_count)
            self.frequencies.append(current_frequency)
            
            return batch_results, current_frequency
        return batch_results, 0
    
    def update_display(self, batch_results, current_frequency):
        """更新显示"""
        if batch_results:
            # 显示最后一次骰子结果
            last_roll, last_is_even = batch_results[-1]
            color = 'green' if last_is_even else 'red'
            even_text = ' (偶数)' if last_is_even else ' (奇数)'
            self.dice_text.set_text(f'{last_roll}{even_text}')
            self.dice_text.set_color(color)
        
        # 更新频率曲线
        self.frequency_line.set_data(self.trials, self.frequencies)
        
        # 更新实时数据显示
        freq_info = f"试验: {self.total_count}/{self.max_trials}\n"
        freq_info += f"当前频率: {current_frequency:.4f}\n"
        freq_info += f"偶数次数: {self.even_count}"
        self.current_freq_text.set_text(freq_info)
        
        # 调整x轴范围以便跟随数据
        if self.total_count > 50:
            self.ax1.set_xlim(max(0, self.total_count - 100), self.total_count + 10)
        
        # 更新统计信息
        if self.total_count > 0:
            stats_info = f"试验次数: {self.total_count}\n"
            stats_info += f"偶数出现: {self.even_count}次\n"
            stats_info += f"当前频率: {current_frequency:.4f}\n"
            stats_info += f"理论概率: 0.5000\n"
            stats_info += f"差值: {abs(current_frequency - 0.5):.4f}"
            self.stats_text.set_text(stats_info)
    
    def animate(self, frame):
        """动画更新函数"""
        if self.is_paused or self.total_count >= self.max_trials:
            return self.frequency_line, self.dice_text, self.stats_text, self.current_freq_text
        
        # 批量模拟骰子投掷
        batch_results, current_frequency = self.update_frequency_batch()
        
        # 每隔一定帧数才更新显示，提高性能
        if frame % self.update_interval == 0:
            self.update_display(batch_results, current_frequency)
        
        return self.frequency_line, self.dice_text, self.stats_text, self.current_freq_text
    
    def start_animation(self):
        """开始动画"""
        print(f"开始动态骰子概率模拟 ({self.speed_mode.upper()} MODE)...")
        print("点击图表可以暂停/继续动画")
        print(f"最大试验次数: {self.max_trials}")
        print("速度参数:", self.speed_params[self.speed_mode])
        
        # 创建动画
        params = self.speed_params[self.speed_mode]
        self.animation = FuncAnimation(
            self.fig, self.animate, frames=None,
            interval=params['interval'], blit=True, repeat=True, cache_frame_data=False
        )
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.show()

def run_fast_simulation(max_trials=1000, speed_mode='fast'):
    """
    运行快速骰子概率模拟
    
    参数:
    max_trials: 最大试验次数
    speed_mode: 速度模式 ('slow', 'normal', 'fast', 'ultra_fast')
    """
    simulator = FastDiceProbability(max_trials, speed_mode)
    simulator.start_animation()

# 提供多种速度选项的便捷函数
def quick_demo():
    """快速演示不同速度模式"""
    print("🎲 骰子概率模拟速度调节演示")
    print("=" * 40)
    print("可用速度模式:")
    print("1. slow - 慢速 (500ms间隔, 逐个更新)")
    print("2. normal - 正常速度 (200ms间隔, 逐个更新)")
    print("3. fast - 快速 (50ms间隔, 批量5个更新)")
    print("4. ultra_fast - 超快速 (10ms间隔, 批量20个更新)")
    print("=" * 40)
    
    mode_map = {
        '1': 'slow',
        '2': 'normal',
        '3': 'fast',
        '4': 'ultra_fast'
    }
    
    choice = input("请选择速度模式 (1-4, 默认3): ").strip() or '3'
    mode = mode_map.get(choice, 'fast')
    
    trials = int(input("请输入试验次数 (默认1000): ") or "1000")
    
    run_fast_simulation(trials, mode)

if __name__ == "__main__":
    quick_demo()

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