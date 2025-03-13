# nonebot-linc

## How to start

1. generate project using `nb create` .
2. create your plugin using `nb plugin create` .
3. writing your plugins under `src/plugins` folder.
4. run your bot using `nb run --reload` .

## Documentation

目前方案是 Nonebot2 (OnebotV11 + FastAPI) + LagrangeDev

见： https://lincdocs.github.io/MdNote_Public/01.%20DesignAndDevelop/Develop/04.%20Project/Platform/SoftCode/ChatBot/%E5%AE%9E%E6%88%98/Nonebot2_Lagrange.html?deep=6

# dot env

这个文件不同步的，需要自行创建：

```ini
ENVIRONMENT=dev
DRIVER=~fastapi
SUPERUSERS=["your qq id"]
deepseek__api_key="sk-xxxxxx" # https://github.com/KomoriDev/nonebot-plugin-deepseek
```
