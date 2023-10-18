import re
import os

owner = 'Reid00'
repo = 'image-host'
branch = 'master'
github = f'github.com/{owner}/{repo}/raw/{branch}'
staticaly = f'cdn.staticaly.com/gh/{owner}/{repo}@{branch}'
chinaJsDelivr = f'jsd.cdn.zzko.cn/gh/{owner}/{repo}@{branch}'
jsDelivr = f'cdn.jsdelivr.net/gh/{owner}/{repo}@{branch}'
basepath = r'C:\Personal\Reid00.github.io.source\content\posts\algo'

def redistribution(basepath):
    for root, dirs, files in os.walk(basepath):
        for file in files:
            if file and os.path.splitext(file)[-1] == '.md':
                filename = os.path.join(root, file)
                with open(filename, encoding="utf-8") as f:
                    d = re.sub(f'{staticaly}', f'{github}', f.read())
                    d = re.sub(f'{chinaJsDelivr}', f'{github}', d)
                    d = re.sub(f'{jsDelivr}', f'{github}', d)
                with open(filename, 'w') as f:
                    f.write(d)


if __name__ == '__main__':
    redistribution(basepath)
