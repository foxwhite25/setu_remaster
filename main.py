import asyncio
import os
import time

import hoshino
from hoshino.util import DailyNumberLimiter

from .data import get_random_setu, get_search_setu, download_illust, get_illust_b64, format_illust
from .lib import config_with_key, RecordDAO, path_dirname, illust_path

sv = hoshino.Service('setu_remaster', bundle='pcr娱乐')
tlmt = hoshino.util.DailyNumberLimiter(config_with_key('daily_max'))
flmt = hoshino.util.FreqLimiter(config_with_key('freq_limit'))
_tlmt = DailyNumberLimiter(5)
DB_PATH = os.path.expanduser("~/.hoshino/illust.db")
db = RecordDAO(DB_PATH)


def check_lmt(uid: int, num: int) -> str:
    if uid in hoshino.config.SUPERUSERS:
        return ''
    if not tlmt.check(uid):
        return f"您今天已经冲过{config_with_key('daily_max')}次了,请明天再来!"
    if num > 1 and (config_with_key('daily_max') - tlmt.get_num(uid)) < num:
        return f"您今天的剩余次数为{config_with_key('daily_max') - tlmt.get_num(uid)}次,已不足{num}次,请节制!"
    if not flmt.check(uid):
        return f'您冲的太快了,请等待{round(flmt.left_time(uid))}秒!'
    flmt.start_cd(uid)
    return ''


@sv.on_prefix('illust')
async def group_setting(bot, ev):
    gid = ev['group_id']
    is_su = hoshino.priv.check_priv(ev, hoshino.priv.SUPERUSER)
    args = ev.message.extract_plain_text().split()
    setting = db.fetch_setting(gid)
    msg = ''
    if not is_su:
        await bot.send(ev, "invalid permission")
        return
    db.update_setting_version(gid)
    if args[0] == "get":
        msg = f"Group {gid} setting:"
        for name, data in setting.items():
            msg += f"\n{name} : {data}"
        print(msg)
        await bot.send(ev, msg)
        return
    elif args[0] == "set":
        if args[1] not in setting:
            await bot.send(ev, "invalid parameter")
            return
        if isinstance(setting[args[1]], bool):
            if args[2].lower() == "true".lower():
                setting[args[1]] = True
                msg = f"Group {gid} option {args[1]} set to True"
            elif args[2].lower() == "false".lower():
                setting[args[1]] = False
                msg = f"Group {gid} option {args[1]} set to False"
            else:
                msg = "invalid type , must be a 'bool'"
        elif isinstance(setting[args[1]], int):
            if args[2].isnumeric():
                setting[args[1]] = int(args[2])
                msg = f"Group {gid} option {args[1]} set to {args[2]}"
            else:
                msg = "invalid type , must be a 'int'"
        elif isinstance(setting[args[1]], str):
            setting[args[1]] = args[2]
            msg = f"Group {gid} option {args[1]} set to {args[2]}"
        db.update_setting(gid, setting)
        await bot.send(ev, msg)
        return
    elif args[0] == 'warehouse':
        num = len(os.listdir(os.path.join(path_dirname, 'illust')))
        await bot.send(ev, f"Current illust count : {num}")
        return
    else:
        await bot.send(ev, "invalid parameter")
        return


@sv.on_rex(r'^不够[涩瑟色]|^再来[点张份]|^[涩瑟色]图$|^[再]?来?(\d*)?[份点张]([涩色瑟]图)')
async def send_random_setu(bot, ev):
    uid = ev['user_id']
    gid = ev['group_id']
    setting = db.fetch_setting(gid)
    num = 1
    match = ev['match']
    try:
        num = int(match.group(1))
    except Exception:
        pass
    msg = check_lmt(uid, num)
    if msg:
        await bot.send(ev, msg)
        return
    b64_list = get_random_setu(num)
    await send_illust_list(uid, gid, setting, b64_list, bot, ev)


@sv.on_rex(r'^搜[索]?(\d*)[份张]*(.*?)[涩瑟色]图(.*)')
async def send_search_setu(bot, ev):
    uid = ev['user_id']
    gid = ev['group_id']
    setting = db.fetch_setting(gid)
    keyword = ev['match'].group(2) or ev['match'].group(3)
    if not keyword:
        await bot.send(ev, '需要提供关键字')
        return
    keyword = keyword.strip()
    num = ev['match'].group(1)
    if num:
        num = int(num.strip())
    else:
        num = 1
    msg = check_lmt(uid, num)
    if msg:
        await bot.send(ev, msg)
        return
    b64_list = get_search_setu(keyword, num)
    await send_illust_list(uid, gid, setting, b64_list, bot, ev)


@sv.on_prefix(r'提取图片')
async def get_illust(bot, ev):
    uid = ev['user_id']
    gid = ev['group_id']
    setting = db.fetch_setting(gid)
    args = ev.message.extract_plain_text().split()
    b64_list = []
    for arg in args:
        if not arg.isnumeric():
            await bot.send(ev, "id应为数字")
            return
        illust = download_illust(arg)
        if not illust:
            await bot.send(ev, f"找不到id为{arg}的图片")
            return
        b64 = get_illust_b64(arg)
        b64_list.append((illust, b64))
    await send_illust_list(uid, gid, setting, b64_list, bot, ev)


async def send_illust_list(uid, gid, setting, b64_list, bot, ev):
    if setting['foward']:
        foward_list = []
        for illust, b64 in b64_list:
            data = {
                "type": "node",
                "data": {
                    "name": '某lsp',
                    "uin": str(uid),
                    "content": format_illust(illust, b64, gid)
                }
            }
            foward_list.append(data)
        tlmt.increase(uid, len(foward_list))
        msg_id = await bot.send_group_forward_msg(group_id=gid, messages=foward_list)
        if setting['withdraw'] and setting['withdraw'] > 0:
            await asyncio.sleep(setting['withdraw'])
            try:
                await bot.delete_msg(self_id=ev['self_id'], message_id=msg_id)
            except Exception:
                print('撤回失败')
        else:
            return
    else:
        result_list = []
        for illust, b64 in b64_list:
            result_list.append(await bot.send(ev, format_illust(illust, b64, gid)))
            await asyncio.sleep(0.5)
        if setting['withdraw'] and setting['withdraw'] > 0:
            await asyncio.sleep(setting['withdraw'])
            for result in result_list:
                try:
                    await bot.delete_msg(self_id=ev['self_id'], message_id=result['message_id'])
                except Exception:
                    print('撤回失败')


@sv.scheduled_job('cron', hour='*')
async def delete_old_illust():
    now = time.time()
    for f in os.listdir(illust_path):
        f = os.path.join(illust_path,f)
        if os.stat(f).st_atime < now - 3600 and os.path.isfile(f):
            os.remove(f)
