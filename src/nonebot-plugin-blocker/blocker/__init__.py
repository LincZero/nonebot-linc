from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="blocker",
    description="拦截器/别名器。最高优先级，静态/动态拦截插件 (相当于开关插件) 以及增加别名",
    usage="暂静态生效，等待开发动态功能",
    config=Config,
)

config = get_plugin_config(Config)

# --------------------------- 超级用户专用 ---------------------------------------

from nonebot import get_driver, logger
from nonebot.exception import IgnoredException
from nonebot.message import event_preprocessor, run_preprocessor
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent

superusers = set(map(str, get_driver().config.superusers)) # 超级用户列表

@event_preprocessor
async def blocker(event: Event):
    # 拦截所有非艾特自己的信息
    # if not event.is_tome(): raise IgnoredException("some reason1")

    # 拦截所有非超管发言
    # if hasattr(event, 'user_id'):
    user_id = getattr(event, 'user_id', None)
    if user_id is not None and str(user_id) not in superusers:
        # logger.info(f'拦截, {user_id}, {event.user_id}, {event.get_user_id}')
        raise IgnoredException("some reason2")

# --------------------------- gpt插件专用 ---------------------------------------

# import os
# from nonebot_plugin_session import EventSession
from copy import deepcopy
from nonebot.matcher import Matcher
from nonebot.message import event_preprocessor, run_preprocessor, handle_event
from nonebot.typing import T_State
from nonebot.adapters import Event
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent

from nonebot import require
require("nonebot_plugin_alconna")
from nonebot_plugin_alconna.uniseg import UniMsg

# 处理gpt插件的上下文，将群昵称注入deepseek__prompt中
@run_preprocessor
async def _(matcher: Matcher, bot: Bot, state: T_State,
    event: Event, event_qq: GroupMessageEvent, msg: UniMsg
):  
    if '/dp' in str(event.get_message()): # 不能用 /ds 开头的内容，不然会重复出现两次相同的事件 (不知道deepseek里面做了什么操作导致会这样)
        if hasattr(event, "_is_fake"):
            logger.debug(f'blocker.ds 2, is_fake')
            return

        # 如果是比较慢的模型，可以先回应安抚一下用户
        # await matcher.send('稍等')

        # 注入群名
        group_info = await bot.get_group_info(group_id=event_qq.group_id)
        group_name = group_info.get("group_name", "未知群组")

        # 只使用其中一个就可以了
        # event.get_message()[0] = str(event.get_message()[0]).replace('/ds', f'/ds 下面是群组"{group_name}"中的提问:\n') # 不生效
        msg[0] = msg[0].replace("/dp", f'/ds 下面是是群组"{group_name}"中的提问:\n') # 生效
        # event_qq.raw_message = event_qq.raw_message.replace('/ds', f'/ds 下面是是群组"{group_name}"中的提问:\n') # 不生效 (仅于其他onebot插件才生效)
        logger.debug(f'''
            blocker.ds
            msg_event: {event.get_message()}
            msg_uni: {msg}
            msg_qq: {event_qq.raw_message}
        ''')
        fake_event = deepcopy(event)
        setattr(fake_event, "_is_fake", True)
        await handle_event(bot, fake_event) # 修改的是副本，必须拦截并重新抛出事件
        raise IgnoredException("some reason")
    pass
