"""
PySide6 信号显示程序 - 修复随机数据不变的问题
根据您提供的界面图片重新创建
"""

import sys
import numpy as np
from datetime import datetime
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPushButton, QTextEdit, QLabel, 
                              QComboBox, QGroupBox, QStatusBar, QMessageBox)
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QFont, QFontDatabase, QColor, QPalette
from PySide6.QtCore import QDateTime
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class SignalDisplayWidget(FigureCanvas):
    """信号显示组件"""
    def __init__(self, parent=None, width=8, height=4, dpi=100):
        # 创建图形
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='white')
        self.ax = self.fig.add_subplot(111)
        
        # 设置中文字体
        self.setup_chinese_font()
        
        super().__init__(self.fig)
        self.setParent(parent)
        
        # 设置图形样式
        self.ax.set_facecolor('#f8f9fa')
        self.ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        
        # 初始化图形
        self.current_signal_type = "random"
        self.plot_signal("random")
    
    def setup_chinese_font(self):
        """设置中文字体"""
        # 尝试多种字体
        font_options = [
            'Microsoft YaHei',  # Windows雅黑
            'SimHei',           # 黑体
            'SimSun',           # 宋体
            'Arial Unicode MS', # Arial Unicode
            'DejaVu Sans'       # 后备字体
        ]
        
        plt.rcParams['font.sans-serif'] = font_options
        plt.rcParams['axes.unicode_minus'] = False
    
    def plot_signal(self, signal_type="random", frequency=1.0, amplitude=1.0):
        """绘制信号"""
        # 生成时间序列
        t = np.linspace(0, 10, 1000, endpoint=False)
        
        # 清除之前的图形
        self.ax.clear()
        
        # 根据信号类型生成数据
        if signal_type == "square":
            # 方波信号
            square_wave = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
            self.ax.plot(t, square_wave, 'b-', linewidth=1.5, label='方波信号')
            title = '方波信号'
            
        elif signal_type == "sine":
            # 正弦波
            sine_wave = amplitude * np.sin(2 * np.pi * frequency * t)
            self.ax.plot(t, sine_wave, 'r-', linewidth=1.5, label='正弦波')
            title = '正弦波'
            
        else:  # 随机信号
            # 每次都生成新的随机种子，确保数据变化
            np.random.seed()  # 使用系统时间作为种子
            random.seed()      # 也设置Python内置random的种子
            
            # 生成随机游走信号
            random_walk = np.zeros(1000)
            for i in range(1, 1000):
                random_walk[i] = random_walk[i-1] + np.random.randn() * 0.1
            
            # 添加一些随机波动
            noise = np.random.randn(1000) * 0.05
            random_walk += noise
            
            # 归一化到-1到2的范围
            random_walk = (random_walk - random_walk.min()) / (random_walk.max() - random_walk.min())
            random_walk = random_walk * 3 - 1  # 缩放到-1到2的范围
            
            self.ax.plot(t, random_walk, 'g-', linewidth=1.5, label='随机信号')
            title = '随机信号'
        
        # 设置图形属性
        self.ax.set_xlabel('时间 (秒)', fontsize=10)
        self.ax.set_ylabel('幅度', fontsize=10)
        self.ax.set_title(title, fontsize=12, fontweight='bold')
        
        # 设置坐标轴范围（与图片一致）
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(-1, 2)
        
        # 设置Y轴刻度
        self.ax.set_yticks([-1.0, -0.5, 0, 0.5, 1.0, 1.5, 2.0])
        
        # 添加网格
        self.ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
        
        # 添加图例
        self.ax.legend(loc='upper right', fontsize=9)
        
        # 调整布局
        self.fig.tight_layout()
        
        # 保存当前信号类型
        self.current_signal_type = signal_type
        
        # 重绘图形
        self.draw()
    
    def update_signal(self, signal_type="random"):
        """更新信号显示"""
        self.plot_signal(signal_type)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 初始化计数器
        self.counter = 0
        self.is_running = False
        
        # 设置字体
        self.setup_fonts()
        
        # 初始化UI
        self.init_ui()
        
        # 设置定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # 每秒更新
        
        # 自动更新定时器（用于随机信号）
        self.auto_update_timer = QTimer()
        self.auto_update_timer.timeout.connect(self.auto_update_signal)
        
    def setup_fonts(self):
        """设置中文字体"""
        # 尝试加载系统字体
        font_families = ["Microsoft YaHei", "SimHei", "SimSun", "Arial"]
        
        for font_family in font_families:
            font = QFont(font_family)
            if font.exactMatch():
                QApplication.setFont(font)
                print(f"使用字体: {font_family}")
                break
        
        # 设置全局字体
        app_font = QApplication.font()
        app_font.setPointSize(9)
        QApplication.setFont(app_font)
    
    def init_ui(self):
        """初始化用户界面"""
        # 设置窗口属性
        self.setWindowTitle('信号显示与控制程序')
        self.setGeometry(100, 100, 900, 700)
        
        # 设置背景色
        self.setStyleSheet("background-color: #f0f0f0;")
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # 1. 控制面板
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel)
        
        # 2. 波形显示区域
        wave_panel = self.create_wave_panel()
        main_layout.addWidget(wave_panel, 1)  # 1表示可拉伸
        
        # 3. 操作日志区域
        log_panel = self.create_log_panel()
        main_layout.addWidget(log_panel)
        
        # 4. 状态栏
        self.create_status_bar()
        
    def create_control_panel(self):
        """创建控制面板"""
        panel = QGroupBox("控制面板")
        panel.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setSpacing(15)
        
        # 图形类型选择
        layout.addWidget(QLabel("图形类型:"))
        
        self.combo_graph_type = QComboBox()
        self.combo_graph_type.addItems(["随机信号", "正弦波", "方波"])
        self.combo_graph_type.setCurrentText("随机信号")
        self.combo_graph_type.setMinimumWidth(150)
        self.combo_graph_type.currentTextChanged.connect(self.on_graph_type_changed)
        layout.addWidget(self.combo_graph_type)
        
        # 添加弹性空间
        layout.addStretch()
        
        # 开始按钮
        self.btn_start = QPushButton("开始")
        self.btn_start.setMinimumWidth(80)
        self.btn_start.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.btn_start.clicked.connect(self.on_start_clicked)
        layout.addWidget(self.btn_start)
        
        # 停止按钮
        self.btn_stop = QPushButton("停止")
        self.btn_stop.setMinimumWidth(80)
        self.btn_stop.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
        """)
        self.btn_stop.clicked.connect(self.on_stop_clicked)
        layout.addWidget(self.btn_stop)
        
        # 清除按钮
        self.btn_clear = QPushButton("清除")
        self.btn_clear.setMinimumWidth(80)
        self.btn_clear.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        self.btn_clear.clicked.connect(self.on_clear_clicked)
        layout.addWidget(self.btn_clear)
        
        panel.setLayout(layout)
        return panel
    
    def create_wave_panel(self):
        """创建波形显示面板"""
        panel = QGroupBox("波形显示")
        panel.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # 创建信号显示图形
        self.canvas = SignalDisplayWidget(self, width=8, height=4)
        layout.addWidget(self.canvas)
        
        panel.setLayout(layout)
        return panel
    
    def create_log_panel(self):
        """创建操作日志面板"""
        panel = QGroupBox("操作日志")
        panel.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout()
        
        self.text_log = QTextEdit()
        self.text_log.setReadOnly(True)
        self.text_log.setMaximumHeight(150)
        self.text_log.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 3px;
                font-family: 'Consolas', 'Microsoft YaHei';
                font-size: 9pt;
                padding: 5px;
            }
        """)
        
        # 添加初始日志
        current_time = datetime.now().strftime("%H:%M:%S")
        self.text_log.append(f"[{current_time}] 程序启动")
        self.text_log.append(f"[{current_time}] 当前图形: 随机信号")
        
        layout.addWidget(self.text_log)
        panel.setLayout(layout)
        return panel
    
    def create_status_bar(self):
        """创建状态栏"""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        # 状态标签
        self.label_status = QLabel("状态: 就绪")
        self.label_status.setStyleSheet("font-weight: bold; color: #4CAF50;")
        status_bar.addWidget(self.label_status)
        
        # 添加分隔符
        status_bar.addPermanentWidget(QLabel(" | "))
        
        # 时间标签
        self.label_time = QLabel("时间: 00:00:00")
        self.label_time.setStyleSheet("font-weight: bold;")
        status_bar.addPermanentWidget(self.label_time)
        
        # 添加分隔符
        status_bar.addPermanentWidget(QLabel(" | "))
        
        # 计数标签
        self.label_counter = QLabel("计数: 0")
        self.label_counter.setStyleSheet("font-weight: bold;")
        status_bar.addPermanentWidget(self.label_counter)
    
    def on_start_clicked(self):
        """开始按钮点击事件"""
        self.counter += 1
        current_time = datetime.now().strftime("%H:%M:%S")
        
        # 更新日志
        self.text_log.append(f"[{current_time}] 任务开始 - 第{self.counter}次")
        
        # 滚动到底部
        scrollbar = self.text_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
        # 更新状态
        self.label_status.setText("状态: 运行中")
        self.label_status.setStyleSheet("font-weight: bold; color: #FF9800;")
        self.label_counter.setText(f"计数: {self.counter}")
        
        # 获取当前信号类型
        signal_type_map = {
            "随机信号": "random",
            "正弦波": "sine",
            "方波": "square"
        }
        
        current_type = self.combo_graph_type.currentText()
        signal_type = signal_type_map.get(current_type, "random")
        
        # 生成新的信号
        if signal_type == "random":
            # 对于随机信号，每次点击都生成新的随机数据
            self.canvas.plot_signal("random")
        else:
            # 对于其他信号，也重新生成
            self.canvas.plot_signal(signal_type)
        
        # 如果是随机信号，启动自动更新
        if signal_type == "random" and not self.is_running:
            self.is_running = True
            self.auto_update_timer.start(100)  # 每100毫秒更新一次
    
    def on_stop_clicked(self):
        """停止按钮点击事件"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.text_log.append(f"[{current_time}] 任务停止")
        
        # 滚动到底部
        scrollbar = self.text_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
        # 更新状态
        self.label_status.setText("状态: 已停止")
        self.label_status.setStyleSheet("font-weight: bold; color: #f44336;")
        
        # 停止自动更新
        self.is_running = False
        self.auto_update_timer.stop()
    
    def on_clear_clicked(self):
        """清除按钮点击事件"""
        # 确认清除
        reply = QMessageBox.question(
            self, '确认清除',
            '确定要清除所有日志和计数吗？',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.text_log.clear()
            self.counter = 0
            self.label_counter.setText("计数: 0")
            self.label_status.setText("状态: 就绪")
            self.label_status.setStyleSheet("font-weight: bold; color: #4CAF50;")
            
            current_time = datetime.now().strftime("%H:%M:%S")
            self.text_log.append(f"[{current_time}] 日志已清除")
    
    def on_graph_type_changed(self, text):
        """图形类型改变事件"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.text_log.append(f"[{current_time}] 切换图形类型: {text}")
        
        # 滚动到底部
        scrollbar = self.text_log.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
        # 更新图形
        signal_type_map = {
            "随机信号": "random",
            "正弦波": "sine",
            "方波": "square"
        }
        
        signal_type = signal_type_map.get(text, "random")
        self.canvas.plot_signal(signal_type)
        
        # 如果切换到随机信号且正在运行，启动自动更新
        if signal_type == "random" and self.is_running:
            if not self.auto_update_timer.isActive():
                self.auto_update_timer.start(100)
        else:
            # 其他信号类型停止自动更新
            if self.auto_update_timer.isActive():
                self.auto_update_timer.stop()
    
    def auto_update_signal(self):
        """自动更新信号（仅用于随机信号）"""
        if self.is_running and self.combo_graph_type.currentText() == "随机信号":
            # 生成新的随机数据
            self.canvas.plot_signal("random")
            
            # 可选：在日志中添加更新记录
            # current_time = datetime.now().strftime("%H:%M:%S")
            # self.text_log.append(f"[{current_time}] 随机信号已更新")
    
    def update_time(self):
        """更新时间显示"""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.label_time.setText(f"时间: {current_time}")

def main():
    """主函数"""
    # 创建应用实例
    app = QApplication(sys.argv)
    
    # 设置应用程序名称
    app.setApplicationName("信号显示与控制程序")
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    # 执行应用程序
    sys.exit(app.exec())

if __name__ == "__main__":
    main()