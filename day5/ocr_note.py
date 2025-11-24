import os
import datetime
from PIL import ImageGrab
import pytesseract
from pynput import keyboard
import tkinter as tk
from tkinter import messagebox
import queue # 导入队列模块
import threading # 导入线程模块

# 设置文件路径和日期
today = datetime.date.today().isoformat()
# 笔记文件保存路径：~/Desktop/YYYY-MM-DD笔记.md
note_file = os.path.expanduser(f"~/Desktop/{today}笔记.md")

# 定义一个队列，用于线程间通信
task_queue = queue.Queue()

def screenshot_and_ocr():
    """执行截图、OCR识别和保存笔记的功能"""
    try:
        # Tkinter UI 必须在主线程中创建，这里是安全的，因为它是从主线程被调用
        root = tk.Tk()
        root.withdraw() # 隐藏主窗口

        # 提示用户准备截图
        messagebox.showinfo("OCR 截图", "点击'确定'开始截图 (将截取整个屏幕进行识别)")

        # 截图（ImageGrab.grab() 截取整个屏幕）
        screenshot = ImageGrab.grab()

        # OCR 识别
        text = pytesseract.image_to_string(screenshot, lang='chi_sim+eng')

        # 保存截图文件
        screenshot_path = os.path.expanduser(f"~/Desktop/{today}_OCR_截图.png")
        screenshot.save(screenshot_path)

        # 保存识别结果到笔记文件
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        with open(note_file, 'a', encoding='utf-8') as f:
            f.write(f"\n\n---\n## {timestamp} 截图笔记\n")
            f.write(f"**识别文字：**\n{text.strip()}\n")
            f.write(f"**截图路径：** {screenshot_path}\n")

        print(f"\n[成功] 识别结果已保存到 {note_file}")
        print(f"[成功] 截图已保存到 {screenshot_path}")

        # 结果提示
        messagebox.showinfo("OCR 成功", f"文字已识别并保存到笔记！\n截图: {screenshot_path}")
        root.destroy() # 关闭 Tkinter 实例

    except Exception as e:
        print(f"\n[错误] OCR 过程中出错了：{e}")
        # 如果是 Tesseract 未找到
        if 'tesseract is not installed or it\'s not in your PATH' in str(e):
             messagebox.showerror("OCR 错误", "Tesseract 引擎未找到。请使用 'brew install tesseract' 安装。")
        else:
             messagebox.showerror("OCR 错误", f"发生未知错误: {e}")

def on_activate():
    """快捷键触发时执行的函数 (运行在 pynput 线程中)"""
    print("\n[触发] 快捷键 Ctrl+Shift+S 触发！任务已发送到主线程...")
    # 将任务（要执行的函数）放入队列中
    task_queue.put(screenshot_and_ocr)

# --- 主线程逻辑 ---

print("=========================================================")
print("第5天 OCR笔记神器启动！请授予终端辅助功能权限。")
print(f"按 Ctrl + Shift + S 开始截图识别，笔记将保存到：{note_file}")
print("=========================================================")

# 启动快捷键监听线程
hotkeys_listener = keyboard.GlobalHotKeys({
    '<ctrl>+<shift>+s': on_activate,
})
hotkeys_listener.start()

# 主循环：持续检查队列，安全地执行 UI 任务
while hotkeys_listener.running:
    try:
        # 非阻塞地从队列中获取任务
        task = task_queue.get(timeout=0.1)
        task() # 执行从 pynput 线程传过来的函数
    except queue.Empty:
        # 如果队列为空，继续循环，等待下一个快捷键事件
        pass
    except KeyboardInterrupt:
        # 允许用户按下 Ctrl+C 退出
        hotkeys_listener.stop()
        break

hotkeys_listener.join()
print("\n程序已退出。")