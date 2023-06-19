# coding:utf8
"""
演示常见的文件操作方法
"""
import os, shutil

# 判断是否文件
print(os.path.isfile("E:\\a.txt"))
print(os.path.isfile("E:\\vm"))

# 判断是否文件夹
print(os.path.isdir("E:\\a.txt"))
print(os.path.isdir("E:\\vm"))

# 列出文件夹内容，就是Linux的ls命令
print(os.listdir("E:\\"))   # 列出的是name，名字，不包含绝对路径

# 创建文件夹
# os.mkdir("E:\\test_sh40")

# 判断路径是否存在
print(os.path.exists("E:\\test_sh40"))
print(os.path.exists("E:\\test_sh41"))

# 删除文件
# os.remove("E:\\a.txt")

# 删除文件夹 等同于 rm -r
shutil.rmtree("E:\\test_sh40")
