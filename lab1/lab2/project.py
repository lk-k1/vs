
import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体（可选）
plt.rcParams["font.family"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题

# 1. 创建时间序列
t = np.linspace(0, 2 * np.pi, 1000)  # 从0到2π，1000个点

# 2. 生成连续正弦信号
x_continuous = np.sin(t)  # 基本正弦信号

# 3. 绘制图形
plt.figure(figsize=(10, 5))

# 连续时间正弦信号
plt.subplot(1, 2, 1)
plt.plot(t, x_continuous, 'b-', linewidth=2)
plt.title("连续时间正弦信号")
plt.xlabel("时间 t")
plt.ylabel("幅度")
plt.grid(True) 





"""
import matplotlib.pyplot as plt
import numpy as np

# 1. 定义离散时间点 (n)
n = np.arange(-5, 6, 1)  # 起始， 终止（不含）， 步长

# 2. 定义离散信号的幅值 u[n]
# 这里以一个简单的指数衰减信号为例: u[n] = 0.8^n * u[n]，其中u[n]是单位阶跃信号
u_n = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1])


# 3. 绘制离散信号（茎状图，stem plot）
plt.figure(figsize=(10, 6))  # 设置图像大小
stem_container = plt.stem(n, u_n, linefmt='b-', markerfmt='bo', basefmt='r-')
plt.setp(stem_container[1], 'linewidth', 2)  # 设置茎线宽度
plt.setp(stem_container[0], 'markersize', 6)  # 设置标记点大小

# 4. 添加图形标签和标题
plt.title('u[n]', fontsize=14)
plt.xlabel('Discrete Time Index (n)', fontsize=12)
plt.ylabel('Amplitude u[n]', fontsize=12)
plt.grid(True, which='both', linestyle='--', alpha=0.6)  # 添加网格
plt.axhline(y=0, color='k', linewidth=0.8)  # 在y=0处画一条黑线
plt.axvline(x=0, color='k', linewidth=0.8)  # 在x=0处画一条黑线

# 5. 调整坐标轴范围
plt.xlim([n.min() - 1, n.max() + 1])
plt.ylim([u_n.min() -0.1, u_n.max() + 0.7])

"""




# 6. 显示图形
plt.tight_layout()
plt.show()
