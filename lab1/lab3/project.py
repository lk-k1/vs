#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信号生成器 GUI
功能：生成并显示基本信号（正弦波、方波、三角波、锯齿波、白噪声）
界面包含：信号类型选择、参数设置、控制按钮、信息显示框、图形显示框
"""

import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# === 配置 Matplotlib 中文支持 ===
matplotlib.rcParams["font.family"] = ["SimHei", "Heiti SC", "Microsoft YaHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False

class SignalGeneratorApp:
    """信号生成器主应用类"""
    
    def __init__(self, root):
        """初始化应用"""
        self.root = root
        self.root.title("信号生成器")
        self.root.geometry("900x600")
        
        # 信号数据
        self.signal_data = None
        self.time_axis = None
        
        # 默认参数
        self.default_freq = 5.0
        self.default_amp = 1.0
        self.default_duration = 1.0
        
        # 创建主布局
        self.create_main_layout()
        
        # 生成初始信号
        self.generate_signal()
    
    def create_main_layout(self):
        """创建主界面布局"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # 左侧控制面板
        left_panel = ttk.LabelFrame(main_frame, text="控制面板", padding="10")
        left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        left_panel.columnconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=3)
        
        # 信号类型选择
        self.signal_type_var = tk.StringVar(value="sin")
        type_frame = ttk.LabelFrame(left_panel, text="信号类型", padding="5")
        type_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        signal_types = [
            ("正弦波", "sin"),
            ("方波", "square"),
            ("三角波", "triangle"),
            ("锯齿波", "sawtooth")
        ]
        
        for idx, (name, code) in enumerate(signal_types):
            rb = ttk.Radiobutton(type_frame, text=name, variable=self.signal_type_var, 
                                value=code, command=self.generate_signal)
            rb.grid(row=idx, column=0, sticky=tk.W, padx=5)
        
        # 参数设置
        param_frame = ttk.LabelFrame(left_panel, text="信号参数", padding="5")
        param_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # 频率
        ttk.Label(param_frame, text="频率 (Hz):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.freq_entry = ttk.Entry(param_frame, width=10)
        self.freq_entry.insert(0, str(self.default_freq))
        self.freq_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        # 幅度
        ttk.Label(param_frame, text="幅度:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.amp_entry = ttk.Entry(param_frame, width=10)
        self.amp_entry.insert(0, str(self.default_amp))
        self.amp_entry.grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        # 时长
        ttk.Label(param_frame, text="时长 (s):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.duration_entry = ttk.Entry(param_frame, width=10)
        self.duration_entry.insert(0, str(self.default_duration))
        self.duration_entry.grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        # 控制按钮
        btn_frame = ttk.Frame(left_panel)
        btn_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.generate_btn = ttk.Button(btn_frame, text="生成信号", 
                                       command=self.generate_signal)
        self.generate_btn.grid(row=0, column=0, padx=5)
        
        self.clear_btn = ttk.Button(btn_frame, text="清除图形", 
                                    command=self.clear_plot)
        self.clear_btn.grid(row=0, column=1, padx=5)
        
        # 信息显示框
        info_frame = ttk.LabelFrame(left_panel, text="信号信息", padding="5")
        info_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.info_text = tk.Text(info_frame, height=8, width=35, state=tk.DISABLED)
        self.info_text.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # 右侧图形显示框
        right_panel = ttk.LabelFrame(main_frame, text="信号波形", padding="10")
        right_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        main_frame.rowconfigure(0, weight=1)
        
        # Matplotlib 图形
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def get_parameters(self):
        """获取用户输入的参数"""
        try:
            freq = float(self.freq_entry.get())
            amp = float(self.amp_entry.get())
            duration = float(self.duration_entry.get())
            
            if freq <= 0 or amp <= 0 or duration <= 0:
                messagebox.showerror("错误", "参数必须大于0！")
                return None
            
            return freq, amp, duration
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字！")
            return None
    
    def generate_signal(self):
        """生成信号并更新显示"""
        params = self.get_parameters()
        if params is None:
            return
        
        freq, amp, duration = params
        signal_type = self.signal_type_var.get()
        
        # 生成时间轴
        sampling_rate = 1000
        num_samples = int(sampling_rate * duration)
        self.time_axis = np.linspace(0, duration, num_samples)
        
        # 生成信号
        signal_name = {"sin":"正弦波", "square":"方波", "triangle":"三角波", 
                       "sawtooth":"锯齿波"}[signal_type]
        
        try:
            if signal_type == 'sin':
                self.signal_data = amp * np.sin(2 * np.pi * freq * self.time_axis)
            elif signal_type == 'square':
                self.signal_data = amp * np.sign(np.sin(2 * np.pi * freq * self.time_axis))
            elif signal_type == 'triangle':
                t = self.time_axis * freq
                self.signal_data = amp * (2 * np.abs(2 * (t - np.floor(t + 0.5))) - 1)
            elif signal_type == 'sawtooth':
                t = self.time_axis * freq
                self.signal_data = amp * (2 * (t - np.floor(t)) - 1)

            
            # 更新图形和信息
            self.update_plot(signal_name, freq, amp)
            self.update_info(signal_name, freq, amp, duration, num_samples)
            
        except Exception as e:
            messagebox.showerror("错误", f"生成信号失败: {str(e)}")
    
    def update_plot(self, signal_name, freq, amp):
        """更新图形显示"""
        self.ax.clear()
        self.ax.plot(self.time_axis, self.signal_data, 'b-', linewidth=2)
        self.ax.set_title(f"{signal_name}信号", fontsize=14)
        self.ax.set_xlabel("时间 (s)", fontsize=12)
        self.ax.set_ylabel("幅度", fontsize=12)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_ylim(-amp*1.2, amp*1.2)
        self.figure.tight_layout()
        self.canvas.draw()
    
    def update_info(self, signal_name, freq, amp, duration, num_samples):
        """更新信息显示框"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        
        info = f"信号类型: {signal_name}\n"
        info += f"频率: {freq:.2f} Hz\n"
        info += f"幅度: {amp:.2f}\n"
        info += f"时长: {duration:.2f} s\n"
        info += f"采样率: 1000 Hz\n"
        info += f"样本数: {num_samples}\n"
        if self.signal_data is not None:
            info += f"平均值: {np.mean(self.signal_data):.4f}\n"
            info += f"标准差: {np.std(self.signal_data):.4f}\n"
            info += f"最大值: {np.max(self.signal_data):.4f}\n"
            info += f"最小值: {np.min(self.signal_data):.4f}"
        
        self.info_text.insert(tk.END, info)
        self.info_text.config(state=tk.DISABLED)
    
    def clear_plot(self):
        """清除图形"""
        self.ax.clear()
        self.ax.set_title("信号波形", fontsize=14)
        self.ax.set_xlabel("时间 (s)", fontsize=12)
        self.ax.set_ylabel("幅度", fontsize=12)
        self.ax.grid(True, alpha=0.3)
        self.figure.tight_layout()
        self.canvas.draw()
        
        # 清除信息
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.config(state=tk.DISABLED)
        
        self.signal_data = None
        self.time_axis = None

def main():
    """主函数"""
    root = tk.Tk()
    app = SignalGeneratorApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()