import tkinter as tk
from tkinter import filedialog, messagebox
import os

class DarkNotepad:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Lucasの暗黑记事本 - Day1 打卡")
        self.root.geometry("900x600")
        self.root.configure(bg='#0d1117')
        
        # 文字区
        self.text = tk.Text(
            self.root,
            bg='#1e1e1e', fg='#d4d4d4', insertbackground='white',
            font=("JetBrains Mono", 14), wrap='word', undo=True
        )
        self.text.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 菜单栏
        # menubar = tk.Menu(self.root, bg='#2d2d2d', fg='white')
        menubar = tk.Menu(self.root, bg='#2d2d2d', fg='white', activebackground='#007acc', activeforeground='white', font=('Arial', 12, 'bold'))
        filemenu = tk.Menu(menubar, tearoff=0, bg='#2d2d2d', fg='white')
        filemenu.add_command(label="新建  Ctrl+N", command=self.new_file)
        filemenu.add_command(label="打开  Ctrl+O", command=self.open_file)
        filemenu.add_command(label="保存  Ctrl+S", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=filemenu)
        self.root.config(menu=menubar)
        
        # 快捷键
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        
        # 状态栏
        self.status = tk.Label(self.root, text="就绪 | 行:1 列:1", bg='#007acc', fg='white', anchor='w')
        self.status.pack(fill='x', side='bottom')
        self.text.bind('<KeyRelease>', self.update_status)
        
        self.filepath = None
        self.auto_save()
        
    def update_status(self, event=None):
        row = self.text.index('insert').split('.')[0]
        col = self.text.index('insert').split('.')[1]
        self.status.config(text=f"就绪 | 行:{row} 列:{col} | 字数:{len(self.text.get(1.0,'end'))-1}")

    def new_file(self):
        self.text.delete(1.0, 'end')
        self.filepath = None
        self.root.title("Lucasの暗黑记事本 - 新建")

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("文本文件","*.txt"),("所有文件","*.*")])
        if path:
            with open(path, 'r', encoding='utf-8') as f:
                self.text.delete(1.0, 'end')
                self.text.insert(1.0, f.read())
            self.filepath = path
            self.root.title(f"Lucasの暗黑记事本 - {os.path.basename(path)}")

    def save_file(self):
        if not self.filepath:
            self.filepath = filedialog.asksaveasfilename(defaultextension=".txt")
        if self.filepath:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                f.write(self.text.get(1.0, 'end'))
            messagebox.showinfo("保存成功", "文件已保存！")

    def auto_save(self):
        if self.filepath:
            self.save_file()
        self.root.after(30000, self.auto_save)  # 30秒自动保存一次

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = DarkNotepad()
    app.run()