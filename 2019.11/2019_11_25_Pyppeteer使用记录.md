### Pyppeteer 是什么？

讨论 Pyppeteer 需要先来了解 Puppeteer。

Puppeteer 是谷歌发布的一款“控制”  Chrome 和 Chromium 的开发工具，基于 NodeJS 开发。主要的应用场景是自动化测试。

额外多说一句，自动化测试和爬虫真是一队好基友，能用来做测试的工具，也基本能用来开发爬虫。

Pyppeteer 是 Puppeteer 的 Python 非官方实现，造福了广大 Python 测试（爬虫）开发者。

### 与 Selenium 相比，Pyppeteer 的优势是什么？

一句话总结：不容易被不容易被反爬识别。

Selenium 久经考验，已经发展的比较成熟，应用也比较广泛。但是，Selenium的反爬也很成熟了，很容易被目标网站识别，比如淘宝、美团等。

Selenium 是通过 Webdriver 来操作浏览器，在操作浏览器进行访问、点击等行为时，都会留下痕迹，进而被反爬虫所识别。尽管可以通过 JS 注入的方式，来屏蔽这些特征，但是配置复杂，且不一定能解决问题。

Pyppeteer 作为一个更新的工具，网站反爬对他的防范程度较低，用来爬取数据，可以避免很多麻烦。尽管它也需要通过JS 注入来实现对网站反爬的屏蔽，但是需要配置的地方比较少，一次配置，全局生效，相对更加容易。

### 个人使用Pyppeteer的若干坑记录

1. 异步编程带来的复杂性

	首先，Puppeteer 基于异步进行开发，Pyppeteer 也是。这意味着爬虫需用通过异步的方式来写，对于不太熟悉异步编程的开发者来讲，还是上手的难度。

	其次，在 Python 中， async/await 的写法，对原有的代码侵入性比较大，需要修改的地方比较多。

	再次，由于 Pyppeteer 本身问题比较多，异步编程又额外带来了复杂性，使得程序调试困难，出了问题排查困难。

2. Chromium 版本问题：

	Pyppeteer 在第一次运行时，会自动下载 Chromium，会非常慢。所以需要手动去下载。下载最新版之后，发现报错，运行不了。后来才发现 Pyppeteer 需要指定版本的 Chromium，版本号为： 575458 ，请各位注意。

3. 不稳定：

	Connection is closed 简直是噩梦，即便是按照网上的说法配置，也无法完全避免。

4. 更新缓慢：

	Pyppeteer 库基本上已经不更新了，遗留了大量的问题待解决，也无法适用于最新版本的 Chromium 。总之问题较多，使用 Pyppeteer 大规模的爬取数据，还不太现实。

### Pyppeteer的最佳实践姿势

最佳使用场景：当目标网站使用加密 Cookie  验证方式请求数据（含模拟登陆），且加密过程复杂，期望避免破解 JS 且快速得到 Cookie时，使用 Pyppeteer 是最佳选择。

个人的使用体会是用 Pyppeteer 直接去爬取数据，爬取比较慢且容易报错。整体来说很难保证爬取的效率。所以放弃用直接 Pyppeteer 爬数据的想法。改用 Pyppeteer 来获取 Cookie，然后用 Requests + Cookie 的方式去获取数据。

### 一个完整的获取Cookie的例子

背景描述：

我需要爬取一个网站，该网站在第一次访问时，会通过 JS 生成一串加密后的 Cookie，其他的数据通过api携带此 Cookie 返回数据，无 Cookie 则无法正常返回数据。该网站 JS生成 Cookie 的方式破解起来很麻烦，所以考虑直接通过 Pyppeteer拿到 Cookie 了事。下面是一个例子，传入 URL 和 代理 IP 即可。

```
"""
Description:
Author:qxy
Date: 2019/11/21 4:28 下午
File: get_cookie 
"""

import asyncio
from pyppeteer import launch
import time
import shutil


async def get_cookie(url, ip):  # 启动浏览器
    browser = await launch({
                            'devtools': False,  # 是否打开开发者模式
                            'userDataDir': './userdata', # 在目录下生成cookie文件，下次启动 Chromium 会自动携带已存储的cookie信息
                            "headless": True, # 打开无头模式，注意：在服务器上运行时，devtools也需要关闭
                            'args': [
                                '--disable-extensions',
                                '--disable-bundled-ppapi-flash',
                                '--mute-audio',
                                '--no-sandbox',
                                '--disable-setuid-sandbox',
                                '--disable-infobars',
                                '--proxy-server={}'.format(ip), # 配置代理ip
                            ]})
    page = await browser.newPage()
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36")
    await page.setViewport({'width': 1080, 'height': 960})
    await page.goto(url, timeout=100000)
    cookie_list = await page.cookies()
    cookies = ''
    for cookie in cookie_list:
        coo = "{}={};".format(cookie.get('name'), cookie.get('value'))
        cookies += coo
    print(cookies)
    time.sleep(5)
    await browser.close()
    return cookies
```