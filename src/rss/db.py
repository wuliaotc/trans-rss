import sqlite3
import os

RssCreateTableSQl = """
            CREATE TABLE rss(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT DEFAULT "" NOT NULL,
                url TEXT NOT NULL,
                download_dir TEXT NOT NULL,
                filters TEXT DEFAULT "" NOT NULL,
                enable INTEGER DEFAULT 0 NOT NULL,
                xml TEXT DEFAULT "" NOTNULL,
                last_update_time INTEGER DEFAULT 0 NOT NULL,
                create_time INTEGER NOT NULL,
                update_time INTEGER NOT NULL
            );
            """
TorrentCreateTableSql = """
            CREATE TABLE torrent(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT UNIQUE ,
                create_time INTEGER NOT NULL
            );

"""


class RssSub:
    def __init__(self) -> None:
        pass

    @property
    def id(self) -> int:
        """The id property."""
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def name(self) -> str:
        """The name property."""
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def url(self) -> str:
        """The url property."""
        return self._url

    @url.setter
    def url(self, value: str):
        self._url = value

    @property
    def download_dir(self) -> str:
        """The download_dir property."""
        return self._download_dir

    @download_dir.setter
    def download_dir(self, value: str):
        self._download_dir = value

    @property
    def filters(self) -> str:
        """The filters property."""
        return self._filters

    @filters.setter
    def filters(self, value: str):
        self._filters = value

    @property
    def enable(self) -> bool:
        """The enable property."""
        return self._enable

    @enable.setter
    def enable(self, value: bool):
        self._enable = value

    @property
    def xml(self) -> str:
        """The xml property."""
        return self._xml

    @xml.setter
    def xml(self, value: str):
        self._xml = value

    @property
    def last_update_time(self) -> int:
        """The last_update_time property."""
        return self._last_update_time

    @last_update_time.setter
    def last_update_time(self, value: int):
        self._last_update_time = value

    @property
    def create_time(self) -> int:
        """The create_time property."""
        return self._create_time

    @create_time.setter
    def create_time(self, value: int):
        self._create_time = value

    @property
    def update_time(self) -> int:
        """The update_time property."""
        return self._update_time

    @update_time.setter
    def update_time(self, value: int):
        self._update_time = value


class torrent:
    def __init__(self) -> None:
        pass

    @property
    def id(self) -> int:
        """The id property."""
        return self._id

    @id.setter
    def id(self, value: int):
        self._id = value

    @property
    def key(self) -> str:
        """The key property."""
        return self._key

    @key.setter
    def key(self, value: str):
        self._key = value

    @property
    def create_time(self) -> int:
        """The create_time property."""
        return self._create_time

    @create_time.setter
    def create_time(self, value: int):
        self._create_time = value


# store,showRss
class DBManager:
    DBName = "data.db"
    RssTableName = "rss"
    torrentTableName = "torrent"

    def NewCur(self) -> sqlite3.Cursor:
        return self._dbCon.cursor()

    def __init__(self, configDir: str):
        if not os.path.isdir(configDir):
            os.makedirs(name=configDir)
        dbPath = os.path.join(configDir, self.DBName)
        hasDB = os.path.isfile(dbPath)
        self._dbCon = sqlite3.connect(dbPath)
        if not hasDB:
            cur = self._dbCon.cursor()
            self.initNewDB(cur)
            cur.close()

    @staticmethod
    def initNewDB(cur: sqlite3.Cursor):
        sql = """
            BEGIN;
            {0}
            {1}
        COMMIT;
        """.format(
            RssCreateTableSQl, TorrentCreateTableSql
        )
        cur.executescript(sql)

    def close(self):
        self._dbCon.close()
