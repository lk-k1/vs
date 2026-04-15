import numpy as np
import matplotlib.pyplot as plt

# 设置样式
plt.style.use('seaborn-v0_8-darkgrid')

# 创建图形和子图
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle('Basic Signal Visualization', fontsize=16, fontweight='bold')

# 1. Continuous Cosine Signal
t_continuous = np.linspace(-2*np.pi, 2*np.pi, 1000)
cos_signal = np.cos(2 * np.pi * 1.0 * t_continuous)

axs[0, 0].plot(t_continuous, cos_signal, 'b-', linewidth=2, label='cos(2πt)')
axs[0, 0].set_xlabel('Time (t)', fontsize=12)
axs[0, 0].set_ylabel('Amplitude', fontsize=12)
axs[0, 0].set_title('Continuous Cosine Signal', fontsize=14, fontweight='bold')
axs[0, 0].grid(True, alpha=0.3)
axs[0, 0].legend(loc='upper right')
axs[0, 0].axhline(y=0, color='k', linestyle='-', linewidth=0.5)
axs[0, 0].axvline(x=0, color='k', linestyle='-', linewidth=0.5)

# 2. Discrete Unit Step Signal
n_discrete = np.arange(-10, 11)
unit_step = np.where(n_discrete >= 0, 1, 0)

markerline, stemlines, baseline = axs[0, 1].stem(n_discrete, unit_step, linefmt='g-', 
                                                  markerfmt='go', basefmt='k-', label='u[n]')
plt.setp(stemlines, linewidth=1.5)
plt.setp(markerline, markersize=8)
axs[0, 1].set_xlabel('Sample (n)', fontsize=12)
axs[0, 1].set_ylabel('Amplitude', fontsize=12)
axs[0, 1].set_title('Discrete Unit Step Signal', fontsize=14, fontweight='bold')
axs[0, 1].set_xticks(np.arange(-10, 11, 2))
axs[0, 1].grid(True, alpha=0.3)
axs[0, 1].legend(loc='upper right')
axs[0, 1].set_ylim(-0.2, 1.5)

# 3. Continuous Sawtooth Signal
t_sawtooth = np.linspace(-2, 2, 1000)
sawtooth_signal = 2 * (t_sawtooth - np.floor(t_sawtooth + 0.5))

axs[1, 0].plot(t_sawtooth, sawtooth_signal, 'm-', linewidth=2, label='Sawtooth')
axs[1, 0].set_xlabel('Time (t)', fontsize=12)
axs[1, 0].set_ylabel('Amplitude', fontsize=12)
axs[1, 0].set_title('Continuous Sawtooth Signal', fontsize=14, fontweight='bold')
axs[1, 0].grid(True, alpha=0.3)
axs[1, 0].legend(loc='upper right')
axs[1, 0].axhline(y=0, color='k', linestyle='-', linewidth=0.5)
axs[1, 0].axvline(x=0, color='k', linestyle='-', linewidth=0.5)

# 4. Discrete Unit Impulse Signal
n_impulse = np.arange(-5, 6)
unit_impulse = np.where(n_impulse == 0, 1, 0)

markerline2, stemlines2, baseline2 = axs[1, 1].stem(n_impulse, unit_impulse, linefmt='r-', 
                                                    markerfmt='ro', basefmt='k-', label='δ[n]')
plt.setp(stemlines2, linewidth=1.5)
plt.setp(markerline2, markersize=8)
axs[1, 1].set_xlabel('Sample (n)', fontsize=12)
axs[1, 1].set_ylabel('Amplitude', fontsize=12)
axs[1, 1].set_title('Discrete Unit Impulse Signal', fontsize=14, fontweight='bold')
axs[1, 1].set_xticks(np.arange(-5, 6, 1))
axs[1, 1].grid(True, alpha=0.3)
axs[1, 1].legend(loc='upper right')
axs[1, 1].set_ylim(-0.2, 1.5)

# 调整布局
plt.tight_layout()

# 保存图片
plt.savefig('basic_signals_english.png', dpi=300, bbox_inches='tight')

# 显示图形
plt.show()

print("=" * 60)
print("Signal Information:")
print("=" * 60)
print("1. Continuous Cosine Signal:")
print(f"   Time range: {-2*np.pi:.2f} to {2*np.pi:.2f}")
print(f"   Frequency: 1.0 Hz")
print(f"   Amplitude: 1.0")
print(f"   Samples: {len(t_continuous)}")

print("\n2. Discrete Unit Step Signal:")
print(f"   Time range: {n_discrete[0]} to {n_discrete[-1]}")
print(f"   Step at: n = 0")
print(f"   Signal length: {len(n_discrete)}")

print("\n3. Continuous Sawtooth Signal:")
print(f"   Time range: {t_sawtooth[0]:.2f} to {t_sawtooth[-1]:.2f}")
print(f"   Period: 1")
print(f"   Samples: {len(t_sawtooth)}")

print("\n4. Discrete Unit Impulse Signal:")
print(f"   Time range: {n_impulse[0]} to {n_impulse[-1]}")
print(f"   Impulse at: n = 0")
print(f"   Signal length: {len(n_impulse)}")
print("=" * 60)