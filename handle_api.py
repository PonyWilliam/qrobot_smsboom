# encoding=utf8
# 维护 api.提供去重等功能
from pathlib import Path
import json
from threading import Lock
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import httpx
from httpx import Limits
import asyncio

from utils.sql import Sql
from utils.req import reqFunc, default_header_user_agent

path = Path(__file__).parent.absolute().joinpath("debug", "api.db")

sql = Sql(db_path=path)
sql.newTable()
lock = Lock()
q = Queue()


def read_url() -> str:
    global q
    with open("GETAPI.json", "r", encoding="utf8") as f:
        data = json.load(fp=f)
        for d in data:
            if not (
                (
                    d.startswith("https://") or
                    d.startswith("http://")
                ) and ("[phone]" in d)
            ):
                # print(f"{d}淘汰")
                continue
            q.put(d)
    return q


def test():
    while not q.empty():
        i = q.get()
        if reqFunc(i, "19820294268"):
            with lock:
                sql.update(i)


async def test2():
    while not q.empty():
        i = q.get()
        _i = i.replace("[phone]", "19820294267")
        async with httpx.AsyncClient(headers=default_header_user_agent(), timeout=100, limits=Limits(max_connections=1000, max_keepalive_connections=20), verify=False) as client:
            try:
                await client.get(_i)
                # if r.status_code == 200:
                sql.update(i)
                # logger.info("更新")
            except httpx.HTTPError as why:
                return
            except Exception as e:
                return


async def asMain():
    await asyncio.gather(

        *(
            test2()
            for _ in range(150)
        )

    )


def save_api():
    """保存api到 GETAPI.json 文件"""
    apis = sql.select()
    api_lst = [
        api
        for api in apis
    ]
    with open("GETAPI.json", mode="w", encoding="utf8") as j:
        json.dump(fp=j, obj=api_lst, ensure_ascii=False)


def main():
    read_url()
    # with ThreadPoolExecutor(max_workers=1024) as pool:
    #     for _ in range(1024):
    #         pool.submit(test)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asMain())


if __name__ == "__main__":
    main()
    # read_url()
    save_api()
