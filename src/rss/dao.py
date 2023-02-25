from src.rss.db import DBManager, RssSub, torrent
import os
import time
from sqlite3 import Cursor
import hashlib

RssTableName = "rss"
TorrentTableName = "torrent"
configDir = os.path.expanduser("~/.config/trans-rss")


def NewDBManager():
    global configDir
    return DBManager(configDir=configDir)


def hashTorrentUrl(url: str) -> bytes:
    return hashlib.sha256(url.encode()).digest()


def MarkTorrents(cur: Cursor, urlList: list[str]):
    timestamp = time.time()
    l = list()
    for url in urlList:
        key = hashTorrentUrl(url)
        l.append({"key": key, "create_time": timestamp})
    params = tuple(l)
    sql = """
        INSERT INTO {0}(key,create_time)
        VALUES(:key,:create_time)
    """.format(
        TorrentTableName
    )
    cur.executemany(sql, params)
    cur.connection.commit()


def IsTorrentAdded(cur: Cursor, url: str) -> bool:
    key = hashTorrentUrl(url)
    params = (key,)
    sql = """
        SELECT id FROM {0}
        WHERE key= ?
    """.format(
        TorrentTableName
    )
    cur.execute(sql, params)
    if cur.fetchone():
        return True
    return False


def AddNewRssSub(cur: Cursor, url: str, name: str, download_dir: str, filters: str):
    timestamp = time.time()
    params = (
        {
            "url": url,
            "name": name,
            "download_dir": download_dir,
            "filters": filters,
            "create_time": timestamp,
            "update_time": timestamp,
        },
    )

    sql = """
        INSERT INTO {0}(url,name,download_dir,filters,create_time,update_time) 
        VALUES(:url,:name,:download_dir,:filters,:create_time,:update_time)
        """.format(
        RssTableName
    )
    cur.executemany(sql, params)
    cur.connection.commit()


def UpdateRssSub(
    cur: Cursor, id: int, url: str, name: str, download_dir: str, filters: str
):
    timestamp = time.time()
    params = (
        {
            "id": id,
            "url": url,
            "name": name,
            "download_dir": download_dir,
            "filters": filters,
            "update_time": timestamp,
        },
    )
    sql = """
        UPDATE {0}
        SET url=:url,
            name=:name,
            download_dir=:download_dir,
            filters=:filters,
            update_time=:update_time
        WHERE id=:id
        """.format(
        RssTableName
    )
    cur.executemany(sql, params)
    cur.connection.commit()


def UpdateRssSubXml(cur: Cursor, id: int, xml: str):
    timestamp = time.time()
    params = ({"id": id, "xml": xml, "last_update_time": timestamp},)
    sql = """
        UPDATE {0}
        SET xml=:xml,
            last_update_time=:last_update_time
        WHERE id=:id
        """.format(
        RssTableName
    )
    cur.executemany(sql, params)
    cur.connection.commit()


# TODO page
def ListRssSub(cur: Cursor) -> list[RssSub]:
    sql = """
        SELECT
            id, 
            name, 
            url, 
            download_dir, 
            filters, 
            enable, 
            xml,
            last_update_time, 
            create_time, 
            update_time
        FROM {0}
        """.format(
        RssTableName
    )
    cur.execute(sql)
    res: list[RssSub] = list()
    rows = cur.fetchall()
    for row in rows:
        data = RssSub()

        data.id = row[0]
        data.name = row[1]
        data.url = row[2]
        data.download_dir = row[3]
        data.filters = row[4]
        data.enable = row[5]
        data.xml = row[6]
        data.last_update_time = row[7]
        data.create_time = row[8]
        data.update_time = row[9]

        res.append(data)
    return res


def ListSeenTorrent(cur: Cursor) -> list[torrent]:
    sql = """
        SELECT
            id, 
            key 
        FROM {0}
        """.format(
        RssTableName
    )
    cur.execute(sql)
    res: list[torrent] = list()
    rows = cur.fetchall()
    for row in rows:
        data = torrent()

        data.id = row[0]
        data.key = row[1]

        res.append(data)
    return res
