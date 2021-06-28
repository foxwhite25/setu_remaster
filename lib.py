import datetime
import random
import sqlite3
import os
import pathlib
import ujson as json


path_dirname = os.path.dirname(__file__)
config_path = os.path.join(path_dirname, 'config.json')
illust_path = os.path.join(path_dirname, 'illust')
pathlib.Path(illust_path).mkdir(parents=True, exist_ok=True)


def load_config():
    try:
        with open(config_path, 'r', encoding='utf8') as f:
            config = json.load(f)
            return config
    except Exception as ex:
        print(ex)
        return {}


def save_config(config: dict):
    try:
        with open(config_path, 'w', encoding='utf8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as ex:
        print(ex)
        return False


def config_with_key(key):
    config = load_config()
    return config[key]


def illust_path(illust_id):
    return os.path.join(path_dirname, f'illust/{illust_id}.jpg')


def str_time_prop():
    start_date = int(datetime.datetime.now().timestamp())
    end_date = int(datetime.datetime(2020, 1, 1).timestamp())
    random_date = random.randint(end_date, start_date)
    return datetime.datetime.fromtimestamp(random_date).strftime("%Y-%m-%d")


class RecordDAO:
    def __init__(self, db_path):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._create_table()

    def connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self.connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS gp"
                "(gid INT NOT NULL ,data json NOT NULL , PRIMARY KEY (gid))"
            )

    def fetch_setting(self, gid: int) -> dict:
        with self.connect() as conn:
            i = conn.execute(
                'select data from gp where gid=?', (gid,)
            ).fetchall()
        if not i:
            self.update_setting(gid, config_with_key("default"))
            return config_with_key("default")
        return json.loads(i[0][0])

    def update_setting(self, gid: int, data: dict):
        with self.connect() as conn:
            conn.execute(
                'INSERT OR REPLACE INTO gp (gid,data) VALUES (?,?)', (gid, json.dumps(data))
            )

    def update_setting_version(self, gid: int):
        setting = self.fetch_setting(gid)
        default = config_with_key("default")
        for x, y in default.items():
            if x not in setting:
                setting[x] = y
        self.update_setting(gid, setting)
