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
    name="http_forward",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)



fake_db: Dict[str, int] = {} # 记录用户的调用次数

# 信息响应器 - 命令型 (`/<command> args` 格式)
masterMsg = on_command(
    "hi",
    aliases={"hi"},
    rule=to_me(),
    priority=10,
    block=True
)

# 事件处理函数 (装饰器)
@masterMsg.handle()
async def handle_function(event: MessageEvent, args: Message = CommandArg()):
    # 事件响应器
    print("masterMsg 消息队列", args)
    print("  text 命令跟随的内容", args.extract_plain_text())
    print("event 消息事件", event)
    print("  时间", event.time)
    print("  发送人id", event.get_user_id)
    await masterMsg.finish("hii...")
