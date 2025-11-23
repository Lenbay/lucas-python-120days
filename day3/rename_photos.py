import os

desktop = os.path.expanduser("~/Desktop")
print(desktop)

for filename in os.listdir(desktop):
	if filename.lower().endswith(('.jpg','.jpeg','.png','.gif','.bmp')):
		print(f"发现图片：{filename}")
		name_without_ext = os.path.splitext(filename)
		print(name_without_ext)
		name_without_ext = os.path.splitext(filename)[0]
		print(name_without_ext)
		extension = os.path.splitext(filename)[1]
		print(extension)
		new_filename = name_without_ext+"_Lucas备份"+extension
		print(new_filename)

		old_name = os.path.join(desktop,filename)
		new_name = os.path.join(desktop,new_filename)
		os.rename(old_name,new_name)