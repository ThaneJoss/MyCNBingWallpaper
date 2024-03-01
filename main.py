import requests
import os
import datetime
from PIL import Image
from io import BytesIO
import json 

url='https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'
response = requests.get(url)

imgurl=f'https://www.bing.com{response.json()["images"][0]["url"]}'
imgdate=response.json()["images"][0]["enddate"]

imgtitle = response.json()["images"][0]["title"]
imgcopyright = response.json()["images"][0]["copyright"]

print(f"img title: {imgtitle}\nimg date: {imgdate}\nimg url: {imgurl}\nimg copyright: {imgcopyright}")

#download image
img=requests.get(imgurl)

storepath='./images'

# if folder not exist, create it
if not os.path.exists(storepath):
    os.mkdir(storepath)

img=Image.open(BytesIO(img.content))
save_kwargs = {
    'format': 'JPEG',
    'quality': 'high',
    'progressive': True
}

img.save(f'{storepath}/{imgdate}.jpg',**save_kwargs)

info={f"{imgdate}.jpg":
    {
    'title':imgtitle,
    'date':imgdate,
    'url':imgurl,
    'copyright':imgcopyright
    }
}

with open(f"{storepath}/{imgdate}.json", "w",encoding='utf-8') as f:
    json.dump(info, f)
    

img.save('today.jpg', **save_kwargs)
with open(f"today.txt", "w",encoding='utf-8') as f:
    f.write(f"{imgdate} {imgtitle} {imgcopyright}")


now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(now)

current_timezone = datetime.datetime.now().astimezone().tzinfo


readme=f"""
# My CN Bing Wallpaper
![bing](today.jpg) 
*update time: {now} {current_timezone}*
"""

description="""

这个项目是基于 GitHub Actions 的，旨在简化访问迷人的必应每日图片的过程。每天，必应在其主页展示一张令人惊叹的图片，代表着自然、文化等各个方面。

您可以在 [thanejoss.com](https://cn.thanejoss.com) 浏览完整合集。 *(todo)*

要获取原始图片，请使用以下链接：[今日壁纸](https://cn.bingwallpaper.thanejoss.com)。 *(todo)*

## 关于
该项目提供了一个简单的解决方案，使用 GitHub Actions 自动化流程来获取每日必应壁纸。它在每天 UTC+8 时间 00:00 或每当你向存储库推送提交时运行脚本，获取最新的必应壁纸图片并将其保存在本地，方便您用作桌面背景或其他用途。

## 特点

- 基于 GitHub Actions，自动化获取最新的必应壁纸图片。
- 将图片保存在本地，以便轻松访问。
- 可用于将必应壁纸设置为桌面背景。
- 简单易用的 Python 脚本。

## 使用方法

1. Fork 此存储库。
2. 每天 UTC 时间 16:00 或每当您向存储库推送提交时，脚本将自动运行并获取最新的必应壁纸图片。

## 贡献
欢迎对这个项目进行贡献。如果您发现任何问题或有改进建议，请随时提出问题或提交拉取请求。

---
使用 MyBingWallpaper，通过 GitHub Actions 轻松享受迷人的必应每日图片吧！
"""


with open('./readme.md','w+',encoding='utf-8') as f:
    f.write(readme+description)


