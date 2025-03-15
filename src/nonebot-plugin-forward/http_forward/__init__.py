from typing import Dict
from nonebot import on_command              # 信息响应器
from nonebot import get_plugin_config       # 配置获取
from nonebot.rule import to_me              # 规则 - 艾特自己
from nonebot.plugin import PluginMetadata   # 插件 - 配置元信息
from nonebot.adapters import Message        # 适配器 - 信息
from nonebot.params import CommandArg       # 参数 - 依赖注入
from nonebot.adapters import Event          # 事件
from nonebot.adapters.console import MessageEvent

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="forward",
    description="转发到其他服务上",
    usage="/fw -nf、/fw -ob 等",
    config=Config,
)

# import os
# from nonebot_plugin_session import EventSession
from nonebot import get_driver, logger
from nonebot.exception import IgnoredException
from nonebot.matcher import Matcher
from nonebot.message import event_preprocessor, run_preprocessor, handle_event
from nonebot.typing import T_State
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent

from nonebot import require
require("nonebot_plugin_alconna")
from nonebot_plugin_alconna.uniseg import UniMsg

from copy import deepcopy
import httpx

# 处理gpt插件的上下文，将群昵称注入deepseek__prompt中
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, state: T_State,
    event: Event, event_qq: GroupMessageEvent, msg: UniMsg
):
    """
    备用: 同步方法
    response = httpx.get("https://httpbin.org/get")
    logger.debug(f"同步响应: {response.json()}")
    """
    # 这里异步请求到其他服务里
    if '/fw' in str(event.get_message()) or '/forward' in str(event.get_message()):
        logger.debug(f'forward: {event.get_message()}')

        if ' -httpbin' in str(event.get_message()) or ' -text' in str(event.get_message()):
            async with httpx.AsyncClient() as client:
                response = await client.get("https://httpbin.org/get")
                logger.debug(f"异步响应: {response.json()}")
                await matcher.send("已在控制台输出")

        if ' -nf' in str(event.get_message()):
            async with httpx.AsyncClient() as client:
                response = await client.get("https://httpbin.org/get")
                logger.debug(f"异步响应: {response.json()}")
                await matcher.send("已在控制台输出")

        if ' -ob' in str(event.get_message()):
            key = get_driver().config.forward['ob_key']
            logger.debug(f'ob key: {key}')

            async with httpx.AsyncClient(headers={"Authorization": f"Bearer {key}"}) as client:
                response = await client.get("https://httpbin.org/get")
                logger.debug(f"异步响应: {response.json()}")
                await matcher.send("已在控制台输出")
        
        raise IgnoredException("some reason")
