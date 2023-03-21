# -*- encoding: utf-8 -*-
"""
@File        :test.py
@Time        :2023/03/20 17:50:37
@Author      :Reid
@Version     :1.0
@Desc        :重构post 用的代码
"""

# here put the import lib


import os 
from datetime import datetime
import time


def create_same_file(path):
    g = os.walk(os.path.abspath(path))

    for dirpath, dirnames, filenames in g:
        print("dirpath: ", dirpath, type(dirpath))
        print("dirnames: ", dirnames)
        print("filenames: ", filenames)
        now = time.strftime("%Y%m%d", time.localtime()) 
        for file in filenames:
            print(f"原始文件名: {file}")

            # newname = file.split(".")[0] + "_1" + ".md"
            if file.startswith("202"):
                # 以年月日开头的文件
                newname = now + "-" + "-".join(file.rstrip(".md").split("-")[1:]) + "-1" + ".md"
            else:
                # 不以年月日开头的文件
                newname = now + "-" + file.rstrip(".md") + "-1" + ".md"
            
            os.chdir(r"C:\Hugo\Reid00.github.io.source")
            if dirpath == r"C:\Hugo\Reid00.github.io.source\content\posts":
                cmd = f"hugo new -k default posts/{newname}"
            else:
                cmd = f"hugo new -k ml posts/ml/{newname}"
            os.system(cmd)

            print(f"创建文件: {newname}")

def rm_old_file_and_rename(path):
    g = os.walk(os.path.abspath(path))

    for dirpath, dirnames, filenames in g:
        print("dirpath: ", dirpath, type(dirpath))
        print("dirnames: ", dirnames)
        print("filenames: ", filenames)
        for file in filenames:
            if file.endswith("-1.md"):
                print(f"this file will be rename {file}")
                file_path = os.path.join(dirpath, file)
                new_path = os.path.join(dirpath, file.replace("-1.md", ".md"))
                os.rename(file_path, new_path)
                # return
            # else:
            #     file_path = os.path.join(dirpath, file)
            #     os.remove(file_path)


if __name__ == "__main__":
    # create_same_file(r"C:\Hugo\Reid00.github.io.source\content\posts")
    rm_old_file_and_rename(r"C:\Hugo\Reid00.github.io.source\content\posts")