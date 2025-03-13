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

from nonebot import get_driver, logger
from nonebot.exception import IgnoredException
from nonebot.message import event_preprocessor
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

# import os

# 处理gpt插件的上下文，将群昵称注入deepseek__prompt中
@event_preprocessor
async def group_env(event: GroupMessageEvent, event2: Event, bot: Bot):
    if '/ds' in event.raw_message:
        group_info = await bot.get_group_info(group_id=event.group_id)
        group_name = group_info.get("group_name", "未知群组")
        logger.info(f'event, {event}, {event.group_id}, {group_info}, {group_name}')
        # os.environ["deepseek__prompt"] = f'这是群组"${group_name}"中的提问，请用中文简短回答' # 方法一。无用，不会更新已缓存的配置值
        # get_driver().config.get("deepseek__prompt", None) = f'这是群组"${group_name}"中的提问，请用中文简短回答' # 方法二。报错，表达式不能是赋值目标
        # get_driver().config.deepseek__prompt = f'这是群组"${group_name}"中的提问，请用中文简短回答' # 方法二-2。报错，无法为类型“Config”分配成员“deepseek__prompt”
        # config = get_driver().config; config.deepseek.prompt = f'这是群组"{group_name}"中的提问，请用中文简短回答' # 方法二-3。报错，'dict' object has no attribute 'prompt'
        # event.raw_message = f'prompt: 这是群组"group_name"中的提问，请用中文简短回答\n' + event.raw_message # 方法三。对于我写的其他onebot插件是对的，但对于非onebot会有问题，不通用
    # event.raw_message = event.raw_message + '测试' # 仅对我写的其他onebot插件正确，对其他插件不成功
    message = event2.get_message()
    message.__setattr__('message', event.raw_message + '测试2')
