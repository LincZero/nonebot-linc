# ------------------------ 默认插件部分 ---------------------

from nonebot import get_plugin_config, logger       # 配置获取
from nonebot.plugin import PluginMetadata   # 插件 - 配置元信息

from .config import Config

__plugin_meta__ = PluginMetadata(   # 一些注册信息
    name="my_study_plugin",         # 插件名
    description="",                 # 插件描述
    usage="",                       # 插件用例
    config=Config,
)

config = get_plugin_config(Config)

# ------------------------ 命令型 --------------------------

from typing import Dict
fake_db: Dict[str, int] = {} # 记录用户的调用次数

from nonebot import on_command              # 信息响应器
from nonebot.rule import to_me              # 规则 - 艾特自己
from nonebot.permission import SUPERUSER    # 用于筛选用户

# 信息响应器 - 命令型 (`/<command> args` 格式)
weather = on_command(
    "debug1",                       # id、响应名
    aliases={"weather", "天气"},    # 其他响应名
    # rule=to_me(),                 # 需要私聊或艾特
    priority=10,                    # 优先级10 (越小越优先)
    block=True,                     # 向后阻断传播
    permission=SUPERUSER,
)

from nonebot.adapters import Message        # 适配器 - 信息
from nonebot.params import CommandArg       # 参数 - 依赖注入

# 事件处理函数 (装饰器)
@weather.handle()
async def _(args: Message = CommandArg()):
    # 事件响应器
    logger.info(f'masterMsg 消息队列: {args}')
    logger.info(f'  命令跟随的内容: {args.extract_plain_text()}')
    # print("event 消息事件", event)
    # print("  时间", event.time)
    # print("  发送人id", event.get_user_id)
    # 事件响应器
    # await weather.send("天气是...")
    await weather.finish("debug...")

# ------------------------ 信息事件型 ----------------------

from nonebot import on_message              # 配置获取
from nonebot.adapters import Event          # 事件
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent # 群消息

m = on_message(priority=10, block=False, permission=SUPERUSER)

@m.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if ('/debug2' in event.raw_message):
        logger.info(f'''
            信息: {event.raw_message}
            发送人id: {event.user_id}
            发送时间: {event.time}
            回复: {event.reply}
            发送源id: {event.get_session_id()}
            群id: {event.group_id}''')
        if event.reply:
            logger.info(f'''
                回复: {event.reply}
                信息: {event.reply.message}''')

# ------------------------ ALC型 --------------------------

from nonebot import require
require("nonebot_plugin_alconna")

from nonebot.rule import to_me
from arclet.alconna import Alconna, Args
from nonebot_plugin_alconna import Match, on_alconna

weather = on_alconna( # [!code]
    Alconna("/debug3", Args["location?", str]),
    aliases={"/weather3", "/天气预报3"},
    # rule=to_me(),
)

@weather.handle()
async def handle_function(location: Match[str]):
    if location.available:
        weather.set_path_arg("location", location.result)

@weather.got_path("location", prompt="请输入地名")
async def got_location(location: str):
    if location not in ["北京", "上海", "广州", "深圳"]:
        await weather.reject(f"你想查询的城市 {location} 暂不支持，请重新输入！")
    await weather.finish(f"今天{location}的天气是...")
