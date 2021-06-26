import math
import os.path
import base64
import threading

from lib import *
from pixivpy3 import *
import urllib.request

aapi = AppPixivAPI()
papi = PixivAPI()
aapi.set_accept_language('zh-cn')
if config_with_key("proxy"):  # """Set proxy hosts: eg http://app-api.pixivlite.com"""
    aapi.set_api_proxy(config_with_key("proxy"))
# To get refresh token , ses https://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362
aapi.auth(refresh_token=config_with_key("refresh_token"))
papi.auth(refresh_token=config_with_key("refresh_token"))
DB_PATH = os.path.expanduser("~/.hoshino/rate.db")
db = RecordDAO(DB_PATH)


def get_json_from_id(i):
    return aapi.illust_detail(i)


def calculate_value(illust: dict):
    return illust.total_bookmarks


def search_random_setu(keyword: str, k: int) -> list:
    temp = []
    json_result = aapi.search_illust(keyword, search_target='partial_match_for_tags', sort="date_desc",
                                     end_date=str_time_prop())
    if not json_result.illusts:
        return []
    for n in range(math.ceil(k / 30 * config_with_key("multiply"))):
        for illust in json_result.illusts:
            temp.append((illust, calculate_value(illust)))
        next_qs = aapi.parse_qs(json_result.next_url)
        if not next_qs:
            return temp
        json_result = aapi.search_illust(**next_qs)
    return temp


def sort_best_from_tuple(illust_list: list, k: int, randomness: int) -> list:
    if not illust_list:
        return []
    sorted_temp = list(reversed(sorted(illust_list, key=lambda x: x[1])))[:k * randomness]
    return random.sample(sorted_temp, k=k)


def get_search_setu(keyword: str, k: int) -> list:
    sorted_temp = sort_best_from_tuple(search_random_setu(keyword, k), k, config_with_key("randomness"))
    b64_list = []
    threads = []
    if sorted_temp:
        for illust, view in sorted_temp:
            thread = threading.Thread(target=download_illust, args=(illust.id,))
            threads.append(thread)
            thread.start()
        for i in threads:
            i.join()
        for illust, view in sorted_temp:
            b64_list.append((illust, get_illust_b64(illust.id)))
    return b64_list


def get_random_setu(k: int) -> list:
    sorted_temp = sort_best_from_tuple(recommended_random_setu(k), k, 1)
    b64_list = []
    threads = []
    if sorted_temp:
        for illust, view in sorted_temp:
            thread = threading.Thread(target=download_illust, args=(illust.id,))
            threads.append(thread)
            thread.start()
        for i in threads:
            i.join()
        for illust, view in sorted_temp:
            b64_list.append((illust, get_illust_b64(illust.id)))
    return b64_list


def recommended_random_setu(k: int) -> list:
    temp = []
    json_result = aapi.illust_recommended()
    count = math.ceil(config_with_key("multiply") * k / 3)
    while len(temp) < count:
        for illust in json_result.illusts:
            temp.append((illust, calculate_value(illust)))
        next_qs = aapi.parse_qs(json_result.next_url)
        json_result = aapi.illust_recommended(**next_qs)
    return temp


def download_illust(illust_id: int) -> dict:
    json_result = aapi.illust_detail(illust_id)
    illust = json_result.illust
    if not illust:
        return {}
    if not os.path.isfile(illust_path(illust_id)):
        req = urllib.request.Request(illust.image_urls['medium'],
                                     headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://www.pixiv.net/'})
        with open(illust_path(illust_id), "wb") as f:
            with urllib.request.urlopen(req) as r:
                f.write(r.read())
    return illust


def get_illust_b64(illust_id: int) -> str:
    with open(illust_path(illust_id), "rb") as image_file:
        b64 = base64.b64encode(image_file.read()).decode()
        return b64


def format_illust(illust: dict, b64: str, gid: int) -> str:
    setting = db.fetch_setting(gid)
    if not setting['xml']:
        return f'[CQ:cardimage,file={b64},source={illust.title} (id:{illust.id} author:{illust.user.name})]'
    else:
        return f'title:{illust.title}\nauthor:{illust.user.name}\nid:{illust.id}\n[CQ:image,file=base64://{b64}]'
