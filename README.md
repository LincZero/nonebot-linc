# nonebot-linc

## How to start

1. generate project using `nb create` .
2. create your plugin using `nb plugin create` .
3. writing your plugins under `src/plugins` folder.
4. run your bot using `nb run --reload` .

## Documentation

目前方案是 Nonebot2 (OnebotV11 + FastAPI) + LagrangeDev

见： https://lincdocs.github.io/MdNote_Public/01.%20DesignAndDevelop/Develop/04.%20Project/Platform/SoftCode/ChatBot/%E5%AE%9E%E6%88%98/Nonebot2_Lagrange.html?deep=6

## Config

`.env`

这个文件不同步到git的，需要自行创建：

```ini
# 警告：注释不能是尾注释!!! 不然可能有bug
# adapter: {name = "OneBot V11", module_name = "nonebot.adapters.onebot.v11"},
# driver: fastapi httpx
#
# deepseek相关:
# https://github.com/KomoriDev/nonebot-plugin-deepseek
# 
# ENVIRONMENT=xxx, 对应.env.dev还是.env.prod

ENVIRONMENT=dev
DRIVER=~fastapi
SUPERUSERS=["your qq id"]
deepseek__api_key="sk-xxxxxx"
deepseek__prompt="用英文回答"
```

## Usage

多选一

### venv方法

```bash
./.venv/Scripts/activate

nb run --reload
```

### requirements.txt方法

```bash
python -m venv .venv --prompt nonebot2
./.venv/Scripts/activate
pip --version # pip 24.2. or pip 25.0.1. python.exe -m pip install --upgrade pip
pip install -r .\requirements.txt # pip freeze > requirements.txt

nb run --reload
```

### nb/pip手动安装

```bash
python --version # Python 3.12.7
pip --version # pip 24.2. or pip 25.0.1. python.exe -m pip install --upgrade pip
nb --version # nb: nonebot cli version 1.4.2

pip install nonebot2
# adapters
nb adapter install nonebot-adapter-onebot
# drivers
nb driver install nonebot2[fastapi]
#nb driver install nonebot2[httpx]
#nb driver install nonebot2[websockets]
# plugins (这部分可以根据 nb run --reload 后的报错补充)
nb plugin install nonebot_plugin_status
nb plugin install nonebot_plugin_deepseek
nb plugin install ...

# 好像手动不行? 还是得 pip install -r .\requirements.txt
ImportError: cannot import name 'get_driver' from partially initialized module 'nonebot' (most likely due to a circular import) (H:\Git\Private\Group_LincZero\nonebot-linc2\.venv\Lib\site-packages\nonebot\__init__.py)
```

### 重装迁移

基本同上，但是创建一个新项目。并迁移原来的自定义 `plugins` + `.env` 到新项目。

适合环境重大变更，及跨大版本升级

## deepseek插件的debug

```bash
# take from https://api-docs.deepseek.com/zh-cn/api/get-user-balance
# 或者可以直接用这个网站的请求工具来测试
curl -L -X GET "https://api.deepseek.com/user/balance" -H "Authorization: Bearer sk-d7xxxxxxxxxxxxxxxxxxxxxxxxxxxxd8" -H "Accept: application/json"

# 正常响应类似：
{
  "is_available": true,
  "balance_infos": [
    {
      "currency": "CNY",
      "total_balance": "19.97",
      "granted_balance": "0.00",
      "topped_up_balance": "19.97"
    }
  ]
}
```

## 一些错误的解决

01

```bash
03-14 16:33:53 [WARNING] uvicorn | You must pass the application as an import string to enable 'reload' or 'workers'.
```

时有时没的，很奇怪。然后注意修改 `.env` 不一定生效？（要看一下打印信息）

有次修复是注释掉 `FASTAPI_RELOAD=true` (仅参考)

02

```bash
/deepseek --balance

TypeError: Balance.__init__() got an unexpected keyword argument 'error'
```

deepseek api 错了会导致报错，而不是正常回应api不对，容易判断不出来

03

端口占用问题

```bash
# linux
lsof -i :8000
kill -9 <PID>

# windows
netstat -ano | findstr :8080
taskkill /F /PID <PID>
```

04

.env修改后缓存没变

需要重启整个vscode。缓存是存在vscode里的，而不是项目里
