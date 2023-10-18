import re
import os

owner = 'Reid00'
repo = 'image-host'
branch = 'main'
github = f'github.com/{owner}/{repo}/raw/{branch}'
staticaly = f'cdn.staticaly.com/gh/{owner}/{repo}@{branch}'
chinaJsDelivr = f'jsd.cdn.zzko.cn/gh/{owner}/{repo}@{branch}'
jsDelivr = f'cdn.jsdelivr.net/gh/{owner}/{repo}@{branch}'
basepath = r'C:\Personal\Reid00.github.io.source\content\posts'


"""
github.com/Reid00/image-host/raw/master 
cdn.staticaly.com/gh/Reid00/image-host@master 
jsd.cdn.zzko.cn/gh/Reid00/image-host@master 
dn.jsdelivr.net/gh/Reid00/image-host@master
"""

def redistribution(basepath):
    for root, dirs, files in os.walk(basepath):
        for file in files:
            if file and os.path.splitext(file)[-1] == '.md':
                filename = os.path.join(root, file)
                try:
                    # 尝试使用第一种编码方式打开文件
                    with open(filename, encoding="utf-8") as f:
                        d = re.sub(f'{staticaly}', f'{github}', f.read())
                        d = re.sub(f'{chinaJsDelivr}', f'{github}', d)
                        d = re.sub(f'{jsDelivr}', f'{github}', d)
                    with open(filename, 'w', encoding="utf-8") as f:
                        f.write(d)
                    # print("utf-8 encoding")
                except UnicodeDecodeError:
                    # 如果第一种编码方式无法解码文件，则尝试第二种编码方式
                    try:
                        with open(filename, encoding="gbk") as f:
                                d = re.sub(f'{staticaly}', f'{github}', f.read())
                                d = re.sub(f'{chinaJsDelivr}', f'{github}', d)
                                d = re.sub(f'{jsDelivr}', f'{github}', d)
                        with open(filename, 'w', encoding="utf-8") as f:
                            f.write(d)
                        print("gbk encoding")
                    except UnicodeDecodeError:
                        # 如果仍然无法解码文件，则处理错误或采取其他适当的措施
                        pass
   


if __name__ == '__main__':
    redistribution(basepath)
