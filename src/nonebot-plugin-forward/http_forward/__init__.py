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
    if '/fw' in str(event.get_message()):
        logger.debug(f'forward: {event.get_message()}')

        if '/fw -httpbin' in str(event.get_message()) or ' -text' in str(event.get_message()):
            async with httpx.AsyncClient() as client:
                response = await client.get("https://httpbin.org/get")
                logger.debug(f"异步响应: {response.json()}")
                await matcher.send("已在控制台输出")

        if '/fw -nf' in str(event.get_message()):
            async with httpx.AsyncClient() as client:
                response = await client.get("https://httpbin.org/get")
                logger.debug(f"异步响应: {response.json()}")
                await matcher.send("已在控制台输出")

    if '/ob' in str(event.get_message()):
        key = get_driver().config.forward['ob_key']
        logger.debug(f'ob key: {key}')

        group_info = await bot.get_group_info(group_id=event_qq.group_id)
        group_name = group_info.get("group_name", event_qq.group_id)
        group_msg = f"{event_qq.get_user_id()} {event_qq.time}:\n{str(event.get_message()).replace('/ob ', '', 1)}\n"

        async with httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "text/markdown",
                "accept": "*/*",
            },
            verify=False  # 关闭 SSL 验证
        ) as client:
            # TODO 去掉群名中的非法字符
            response = await client.post(f"https://127.0.0.1:27124/vault/ZChat/{group_name}.md", content=f"{group_msg}\n")
            if response.status_code == 204:
                logger.success(f"forward: {group_name}, {response.status_code}")
            else:
                logger.error(f"forward: {group_name}, {response.status_code}")
        
        raise IgnoredException("some reason")
