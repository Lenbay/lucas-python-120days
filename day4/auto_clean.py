import os
import shutil

desktop = os.path.expanduser("~/Desktop")
print(desktop)

folders = {
    "照片": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.heic'],
    "文档": ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx'],
    "视频": ['.mp4', '.mov', '.avi', '.mkv'],
    "杂项": []  # 其他所有文件都进这里
}

for filename in os.listdir(desktop):
    print(filename)
    file_path = os.path.join(desktop,filename)
    print(file_path)
    if os.path.isdir(file_path) or filename.startswith('.') or filename.endswith('.py'):
        continue

    extension = os.path.splitext(filename)[1].lower()
    if extension in folders['照片']:
        target = os.path.join(desktop,'照片')
    elif extension in folders['文档']:
        target = os.path.join(desktop,'文档')
    elif extension in folders['视频']:
        target = os.path.join(desktop,'视频')
    else:
        target = os.path.join(desktop,'杂项')
    print(f"正在处理：{filename}")

    os.makedirs(target, exist_ok=True)
    shutil.move(file_path, target)