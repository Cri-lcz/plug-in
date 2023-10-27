# encoding=utf8
import requests
from wox import Wox, WoxAPI
import base64
import json
import time
from hashlib import md5

# wox带有python标准库,以下额外导入
import pyperclip
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


# 用户写的Python类必须继承Wox类 https://github.com/qianlifeng/Wox/blob/master/PythonHome/wox.py
# 这里的Wox基类做了一些工作，简化了与Wox通信的步骤。
class Main(Wox):
    def translate(self, key):
        session = requests.session()
        url = "https://dict.youdao.com/webtranslate"
        t = int(time.time() * 1000)
        s = f"client=fanyideskweb&mysticTime={t}&product=webfanyi&key=fsdsogkndfokasodnaso".encode()
        md5_hash = md5()
        md5_hash.update(s)
        sign = md5_hash.hexdigest()
        headers = {
            "Referer": "https://fanyi.youdao.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.41",
            "Cookie": "OUTFOX_SEARCH_USER_ID_NCOO=14414038.481940646; OUTFOX_SEARCH_USER_ID=-1022281879@112.109.214.44; _ga=GA1.2.1636339763.1693477469",
        }
        data = {
            "i": key,
            "from": "auto",
            "to": "",
            "dictResult": "true",
            "keyid": "webfanyi",
            "sign": sign,
            "client": "fanyideskweb",
            "product": "webfanyi",
            "appVersion": "1.0.0",
            "vendor": "web",
            "pointParam": "client,mysticTime,product",
            "mysticTime": t,
            "keyfrom": "fanyi.web",
            "mid": "1",
            "screen": "1",
            "model": "1",
            "network": "wifi",
            "abtest": "0",
            "yduuid": "abcdefg",
        }
        requests.packages.urllib3.disable_warnings()

        # 如果用户配置了代理，那么可以在这里设置。这里的self.proxy来自Wox封装好的对象
        proxies = {}
        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
                "http": "http://{}:{}".format(
                    self.proxy.get("server"), self.proxy.get("port")
                ),
                "http": "https://{}:{}".format(
                    self.proxy.get("server"), self.proxy.get("port")
                ),
            }

        res = session.post(
            url=url, data=data, headers=headers, verify=False, proxies=proxies
        )
        key = "ydsecret://query/key/B*RGygVywfNBwpmBaZg*WT7SIOUP2T0C9WHMZN39j^DAdaZhAnxvGcCY6VYFwnHl"
        iv = "ydsecret://query/iv/C@lZe2YzHtZ2CYgaXKSVfsb7Y4QWHjITPPZ0nQp87fBeJ!Iv6v^6fvi2WN@bYpJ4"

        def md5_(data):
            md5_hash = md5()
            md5_hash.update(data.encode())
            return md5_hash.digest()

        aes = AES.new(md5_(key), AES.MODE_CBC, md5_(iv))
        result = aes.decrypt(base64.b64decode(res.text.encode("utf-8"), altchars=b"-_"))
        result = json.loads(unpad(result, 16).decode())
        ret = [lineDict.get("tgt") for lineDict in result.get("translateResult")[0]]
        self.translate_data = "\n".join(ret)
        return self.translate_data

    # 必须有一个query方法，用户执行查询的时候会自动调用query方法
    def query(self, key):
        bs = self.translate(key)
        results = []
        if bs != None:
            results.append(
                {
                    "Title": bs,
                    "SubTitle": key,
                    "IcoPath": "youdao.png",
                    "JsonRPCAction": {
                        # 这里除了自已定义的方法，还可以调用Wox的API。调用格式如下：Wox.xxxx方法名
                        # 方法名字可以从这里查阅https://github.com/qianlifeng/Wox/blob/master/Wox.Plugin/IPublicAPI.cs 直接同名方法即可
                        "method": "openUrl",
                        # 参数必须以数组的形式传过去
                        "parameters": [bs],
                        # 是否隐藏窗口
                        "dontHideAfterAction": False,
                    },
                }
            )
        return results

    def openUrl(self, parame):
        # open url
        # webbrowser.open(parame)
        # WoxAPI.change_query(parame)
        pyperclip.copy(parame)


# 以下代码是必须的
if __name__ == "__main__":
    Main()
