from asyncio import protocols
import functools
from types import _StaticFunctionType
from typing import Literal
from urllib.parse import uses_query
from src.rss.config import RssSubConfig
import urllib3
import feedparser
import logging
import re, os, pathlib, json
import hashlib
import sqlite3

from src.rss.errors import HttpCodeNotOk, RssPaserError
from transmission_rpc import client

httpPool = urllib3.PoolManager()


def initClient(
    protocol: Literal["http", "https"] = "http",
    username: str | None = None,
    password: str | None = None,
    host: str = "localhost",
    port: int = 9091,
    path: str = "/transmission/rpc",
) -> client.Client:
    return client.Client(
        protocol=protocol,
        username=username,
        password=password,
        host=host,
        port=port,
        path=path,
    )


class RssParser:
    # search for patterns by selected args
    @staticmethod
    def filter(title: str, filterPatterns: list[str]) -> bool:
        for pattern in filterPatterns:
            if re.search(pattern=pattern, string=title):
                return True
        return False

    # # parses and adds torrents from feed
    @staticmethod
    def parseFeed(data: str) -> list:
        feed = feedparser.parse(data)
        if feed.bozo and feed.bozo_exception:
            raise RssPaserError(
                "Error parse feed , {0}".format(str(feed.bozo_exceptio))
            )

        return feed.entries


# TODO: add proxy support
def downloadRss(config: RssSubConfig) -> str:
    if config.proxyConfig is None:
        pass
    url = config.url
    res = httpPool.request(method="GET", url=url)

    if res.status != "200":
        raise HttpCodeNotOk

    return res.data


def downloadTorrent(c: client.Client, torrentUrl: str, download_dir: str):
    c.add_torrent(torrent=torrentUrl, download_dir=download_dir)
