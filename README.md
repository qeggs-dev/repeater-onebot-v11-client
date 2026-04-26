<div align="center">

# @复读机Repeater
**- Only Chat, Focus Chat. -**

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-63b9ff.svg)](https://opensource.org/licenses/MIT) [![Protocol](https://img.shields.io/badge/Protocol-Repeater%20API-brightgreen.svg)](https://github.com/qeggs-dev/repeater-ai-chatbot)

</div>

---

*注：本仓库仅为客户端实现，需要配合[后端项目](#相关仓库)使用*

一个基于[`NoneBot`](https://nonebot.dev/)和[`Repeater Server`](https://github.com/qeggs-dev/repeater-ai-chatbot)开发的 AI QQ Bot
**此仓库仅为 Repeater 的 NoneBot OneBot v11 适配客户端**

---

## Length Score
长度评分系统，用于判断回复是否过长，过长则自动发送图片
长度评分的参数由`main_api.json/text_length_score_config`定义，其包含以下参数：
 - `max_lines`：回复的最大行数
 - `single_line_max`：单行的最大长度
 - `mean_line_max`：平均行的最大长度
 - `total_length`：总长度
 - `threshold`：长度评分阈值，包含`group`和`private`两个参数，分别表示群聊和私聊的阈值

长度评分系统通过以下公式计算：
```python
def length_score(text: str) -> float:
    if len(text) == 0:
        length_score = 0
    else:
        lines = text.splitlines()
        length_score = (
            len(lines) / max_lines +
            (
                max(len(line) for line in lines) / single_line_max +
                sum(len(line) for line in lines) / len(lines) / mean_line_max
            ) / 2 +
            len(text) / total_length
        ) / 3
    return length_score
```
PS: 此处的长度评分函数并非实际算法，仅为演示使用
如果长度评分超过阈值，则会向后端请求将文本渲染为图片，以保证不会影响其他用户正常聊天。

---

## ENV配置

| Name                         | Default                                                                    | Description |
|------------------------------|----------------------------------------------------------------------------|-------------|
| REPEATER_LOGGER_LEVEL        | "INFO"                                                                     | 日志等级，可选值：`TRACE`, `DEBUG`、`INFO`、`WARNING`、`ERROR`、`CRITICAL` |
| REPEATER_LOGGER_FORMAT       | "{time:YYYY-MM-DD HH:mm:ss.SSS} \| {level} \| {extra[module]} - {message}" | 到文件的日志格式，与控制台无关 |
| REPEATER_LOGGER_PATH         | "logs/repeater-log-{time:YYYY-MM-DD-HH-mm-ss}.log"                         | 日志文件的路径 |
| REPEATER_LOGGER_ENABLE_QUEUE | true                                                                       | 是否启用队列模式 |
| REPEATER_LOGGER_DELAY        | true                                                                       | 是否在第一条日志输出时才创建日志文件 |
| REPEATER_LOGGER_ROTATION     | "100 MB"                                                                   | 日志文件的轮换条件，可填时长、大小等数据 |
| REPEATER_LOGGER_RETENTION    | "1 month"                                                                  | 日志文件的保留条件，可填时长、大小等数据 |
| REPEATER_LOGGER_COMPRESSION  | "zip"                                                                      | 日志文件的处理方式 |
| STORAGE_BASE_PATH            | "./storage"                                                                | 存储文件的基础路径 |
| ENVIRONMENT                  | "dev"                                                                      | 该值的内容将决定了程序会进一步读取哪个环境变量文件，如`prod`就是读取`.env.prod`，`dev`就是读取`.env.dev` |
| HOST                         | "0.0.0.0"                                                                  | 主机地址 |
| PORT                         | 8080                                                                       | 端口号 |
| COMMAND_START                | ["/"]                                                                      | 用于触发命令的开始字符 |
| COMMAND_SEP                  | ["."]                                                                      | 用于触发命令的分隔符 |
| BACKEND_BASEURL              | "http://127.0.0.1"                                                         | Repeater Server 的 IP 地址 |
| ONEBOT_ACCESS_TOKEN          | ""                                                                         | OneBot的访问令牌 |
| SUPERUSERS                   | [""]                                                                       | 超级用户列表 |

---

## License
这个项目基于[MIT License](LICENSE)发布。

---

## 依赖
| Name       | Version | License      | License Text Link                                                      | Where it is used              |
|------------|---------|--------------|------------------------------------------------------------------------|-------------------------------|
| httpx      | 0.28.1  | BSD License  | [BSD-3-Clause](https://github.com/encode/httpx/blob/master/LICENSE.md) | *Entire Project*              |
| nonebot    | 2.4.3   | MIT License  | [MIT](https://github.com/nonebot/nonebot2/blob/master/LICENSE)         | *Entire Project*              |
| pydantic   | 2.12.0  | MIT License  | [MIT](https://github.com/pydantic/pydantic/blob/main/LICENSE)          | *Entire Project*              |
| aiofiles   | 25.1.0  | MIT License  | [Apache-2.0](https://github.com/Tinche/aiofiles/blob/main/LICENSE)     | `storage`                     |
| pyyaml     | 6.0.3   | MIT License  | [MIT](https://github.com/yaml/pyyaml/blob/main/LICENSE)                | `storage`                     |
| orjson     | 3.11.3  | Apache Software License; MIT License | [Apache-2.0](https://github.com/ijl/orjson/blob/master/LICENSE-APACHE) / [MIT](https://github.com/ijl/orjson/blob/master/LICENSE-MIT) | `storage` |
| loguru     | 0.7.3   | MIT License  | [MIT](https://github.com/Delgan/loguru/blob/master/LICENSE)            | *Entire Project*              |
| curlify2   | 2.0.0   | MIT License  | [MIT](https://github.com/marcuxyz/curlify2/blob/master/LICENSE)        | *Entire Project*              |

具体依赖的License请查看[LICENSES.md](LICENSES.md)

---

## 配置部署
**推荐 Python3.11 ~ Python3.12 的版本安装**
> PS: 复读机可能会兼容Python3.11以前的版本
> 但我们并未对其进行过测试
> 此处3.11为开发环境版本
> 同时由于 [`PEP 594`](https://peps.python.org/pep-0594/#imghdr) 移除了一些模块
> 因此在本组件迁移之前建议不要超过 Python3.12
> PS: 其他微服务组件不受影响

在目录下执行 `setup.bat` 或 `bash setup.sh`
#### 使用脚手架(nb-cli)创建项目环境
1. 选择simple模板
2. 给项目起个名字（比如`Repeater`）
3. 建议使用FastAPI驱动器
4. **至少必须选择OneBot V11适配器**
5. 输入Yes安装默认依赖
6. 输入Yes安装虚拟环境
7. 如果需要，可以选择内置插件，如echo，*但如果没记错的话我们好像有一个echo了*
8. 在项目目录下，找到`.env`文件
9. 填写 `PORT`(数字), `ONEBOT_ACCESS_TOKEN`(字符串) 等字段配置项
10. 将复读机的NoneBot插件放入项目目录下（通常是`plugins`文件夹下）

执行`{项目名称}/.venv/pip install httpx`安装唯一依赖（此处这个大括号要去掉）
运行`run.py`启动程序

---

## 连接

### 连接OneBot
1. 找到项目目录下的`.env`文件
2. 填写PORT(数字), ONEBOT_ACCESS_TOKEN(字符串) 等字段配置项
3. 执行`run.bat`或`bash run.sh`启动程序
4. 打开OneBot客户端，选择反向WebSocket(部分客户端上称为`WebSocket 客户端`)
5. 填写 `ws_url`(字符串，通常是`ws://127.0.0.1:PORT`，其中`PORT`是你在`.env`文件中填写的端口号)，`token`(字符串，需要与上面的`ONEBOT_ACCESS_TOKEN`一致)
6. 看到NoneBot日志输出中出现`connection open`时, 表示连接成功

### 链接后端
1. 找到项目目录下的`.env`文件
2. 填写`BACKEND_BASEURL`字段配置项 (需要你和后端配置中编写的一致)
3. 执行`run.bat`或`bash run.sh`启动程序

PS: 由于OneBot客户端通常为内网服务，所以默认情况下所有服务都不需要配置公网IP访问
但你需要保证后端可以连接到你设定的API端口，OneBot客户端可以连接到指定社交平台的服务器

---

## 配置文件

main_api.json
```json
{
    // Text Length Score 配置
    "text_length_score_config":{

        // 最大长度阈值
        "max_lines": 5,

        // 每行最大字符数
        "single_line_max": 64,

        // 平均行最大字符数
        "mean_line_max": 24,

        // 总字符数
        "total_length": 400,

        // 评分阈值
        "threshold": {

            // 群聊阈值
            "group": 1.0,

            // 私聊阈值
            "private": 2.64
        }
    },

    // 在仅@且没有任何文本的情况下
    // 返回的消息内容
    "hello_content": "Repeater is Online!",

    // 是hello_content的变种
    // 这里的Key是星期
    // Value是星期对应的消息内容
    "welcome_messages_by_weekday": {
        "4": "Repeater is Online!\n\n疯狂星期四! ! !\n复读机想要 50,000,000 Token ，求求了（>^< ;)"
    },
    // 是否在群聊中让所有人使用同一个上下文
    "usage_group_context": false,

    // Repeater API超时时间
    "server_api_timeout": {

        // 聊天 API 超时
        "chat": 600.0,

        // 上下文操作 API 超时
        "context": 10.0,

        // 提示词操作 API 超时
        "prompt": 10.0,

        // 配置操作 API 超时
        "config": 10.0,

        // 综合数据管理 API 超时
        "data_manager": 10.0,

        // 许可证 API 超时
        "licenses": 10.0,

        // 模型信息 API 超时
        "model_info": 10.0,

        // 状态 API 超时
        "status": 10.0,

        // 版本 API 超时
        "version": 10.0,

        // 变量展开 API 超时
        "variable_expansion": 40.0,

        // 图片渲染 API 超时
        "render": 600.0
    },

    // 在用户输入图片的时候，是否将其下载为 Base64 以防止链接失效
    "use_base64_image_url": false,
    
    // 伪装选项，可能会有一定的反风控效果
    "camouflage": {
        // 限制发送消息的频率
        // 默认 100 次/分钟
        // 如果想关闭可以设置为 null
        "send_msg_limit_speed_per_minute": 100
    },

    // 下载图片的超时时间
    "download_image_timeout": 600.0,

    // 是否使用缩写来显示分支文件大小
    "branch_file_size_use_abbreviation": true,

    // 总计并收缩使用的默认消息内容
    "summarize_and_contract_default_message": "System Message: please sum up all the contents above.",

    // AI 生成内容提示
    "ai_generate_tip": "This content is generated by AI, be aware of authentication.",

    // 是否将用户ID哈希化
    "hash_user_id": false,

    // 是否允许用户构造任意消息发送
    "allow_send_any_message": false,

    // 模型生成的首字超时时间
    // 当到达该时间时，模型并没有生成任何内容
    // 缓冲区是空的
    // 则认为本次请求无法开始生成
    // Client 将向 Repeater Server 申请取消任务
    // 将其设置为 null 可以忽略超时检查
    "model_first_chunk_timeout": 90.0,
    
    // 是否在注册时打印 Handler 信息
    // 默认为 false
    "print_handler_info": false
}
```
配置了一些主要的参数，如文本长度评分、推理模型使用的UID、欢迎消息等。

tts.json
```json
{
    // ChatTTS API 地址
    "base_url": "http://127.0.0.1:9966",

    // ChatTTS API 参数
    "api_args": {

        // 模型名称
        "voice": "265.pt",

        // TTS 语速
        "speed": 6,

        // TTS 模型提示词
        "tts_prompt": "[break_6]",

        // TTS 模型温度
        "temperature": 0.2,

        // TTS 模型Top_P
        "top_p": 0.701,

        // TTS 模型Top_K
        "top_k": 20,

        // TTS 模型生成的最大优化Token数
        "refine_max_new_token": 384,

        // TTS 模型生成最大推理Token数
        "infer_max_new_token": 2048,

        // 文本种子（我不确定这里是文本修饰种子还是TTS种子，不填则随机生成）
        "text_seed": 42,

        // 是否跳过输入优化
        "skip_refine": true,

        // 是否为流式输出
        "is_stream": false,

        // 自定义语音
        "custom_voice": 0
    },
    "timeout": 300.0
}
```
PS：该配置文件是专门用于对接ChatTTS的
如果不需要TTS功能，该部分可以忽略

---

## 命令表

| Command                    | Abridge  | Full Name                 | Type        | Joined Version | Description                   | Parameter Description                     | Remarks |
| :---                       | :---     | :---                      | :---:       | :---           | :---                          | :---                                      | :---    |
| `echo`                     | `echo`   | `Echo`                    | `ECHO`      | 4.0 Beta       | 重复消息                       | 要重复消息内容                             | 重复消息内容，包括特殊消息段，如果输入不跟内容，复读机会等待下一条消息 |
| ` `                        | ` `      | ` `                       | `CHAT`      | 4.0 Beta       | 默认命令，自然语言对话          | 自然语言输入                               | 当@复读机的时候，如果没有命中其他命令就会执行这个 |
| `chat`                     | `c`      | `Chat`                    | `CHAT`      | 4.0 Beta       | 与机器人对话                   | 自然语言输入                               | 强制模型用文字输出，绕过Markdown渲染检查 |
| `keepAnswering`            | `ka`     | `KeepAnswering`           | `CHAT`      | 4.0 Beta       | 持续对话(常规)                 | 无                                        | 无须输入，AI再次回复 |
| `keepReasoning`            | `kr`     | `KeepReasoning`           | `CHAT`      | 4.0 Beta       | 持续对话(推理)                 | 无                                        | 无须输入，AI再次使用推理回复 |
| `renderChat`               | `rc`     | `RenderChat`              | `CHAT`      | 4.0 Beta       | 渲染Markdown回复               | 自然语言输入                               | 强制渲染图片输出 |
| `setRenderStyle`           | `srs`    | `SetRenderStyle`          | `CONFIG`    | 4.0 Beta       | 设置渲染样式                   | 渲染样式名称                               | 设置Markdown图片渲染样式 |
| `npChat`                   | `np`     | `NoPromptChat`            | `CHAT`      | 4.0 Beta       | 不加载提示词进行对话            | 自然语言输入                               | 使用常规模型 |
| `reason`                   | `r`      | `Reason`                  | `CHAT`      | 4.0 Beta       | 使用 Thinking 模式进行推理      | 自然语言输入                               | 开启 `thinking` 参数以激活 Thinking 模式 |
| `setFrequencyPenalty`      | `sfp`    | `SetFrequencyPenalty`     | `CONFIG`    | 4.0 Beta       | 设置频率惩罚                   | `-2`\~`2`的浮点数<br/>或`-200%`\~`200%`的百分比 | 控制着模型输出重复相同内容的可能性 |
| `setPresencePenalty`       | `spp`    | `SetPresencePenalty`      | `CONFIG`    | 4.0 Beta       | 设置存在惩罚                   | `-2`\~`2`的浮点数<br/>或`-200%`\~`200%`的百分比 | 控制着模型谈论新主题的可能性 |
| `setTemperature`           | `st`     | `SetTemperature`          | `CONFIG`    | 4.0 Beta       | 设置温度                       | `0`\~`2`的浮点数<br/>或`0%`\~`200%`的百分比  | 控制着模型生成内容的不确定性 |
| `setPrompt`                | `sp`     | `SetPrompt`               | `PROMPT`    | 4.0 Beta       | 设置提示词                     | 自然语言输入                               | 设置提示词 |
| `changeDefaultPersonality` | `cdp`    | `ChangeDefaultPersonality`| `CONFIG`    | 4.0 Beta       | 修改默认人格                   | 人格预设名称                               | 修改默认人格路由 |
| `deletePrompt`             | `dp`     | `DeletePrompt`            | `PROMPT`    | 4.0 Beta       | 删除提示词                     | 无                                        | 删除提示词 |
| `deleteContext`            | `dc`     | `DeleteContext`           | `CONTEXT`   | 4.0 Beta       | 删除上下文                     | 无                                        | 删除上下文 |
| `varExpand`                | `ve`     | `VarExpand`               | `VAREXPAND` | 4.0 Beta       | 变量展开                       | 文本模板                                  | 变量展开 |
| `setDefaultModel`          | `sdm`    | `SetDefaultModel`         | `CONFIG`    | 4.0 Beta       | 设置默认模型                   | 模型UID                                   | 设置默认使用的模型 |
| `setTopP`                  | `stp`    | `SetTopP`                 | `CONFIG`    | 4.0.1 Beta     | 设置Top_P参数                  | 0\~1的浮点数<br/>或`0%`\~`100%`的百分比    | 设置Top_P参数 |
| `setMaxTokens`             | `smt`    | `SetMaxTokens`            | `CONFIG`    | 4.0.1 Beta     | 设置最大生成tokens数           | 整数，通常最大可达模型上下文窗口长度的一半    | 设置最大生成tokens数 |
| `getContextTotalLength`    | `gctl`   | `GetContextTotalLength`   | `CONTEXT`   | 4.0.1 Beta     | 获取上下文总长度               | 无                                         | 获取上下文总长度 |
| `publicSpaceChat`          | `psc`    | `PublicSpaceChat`         | `CHAT`      | 4.0.2.1 Beta   | 公共空间聊天                   | 自然语言输入                                | 公共空间聊天 |
| `deletePublicSpaceContext` | `dpsc`   | `DeletePublicSpaceContext`| `CONTEXT`   | 4.0.2.1 Beta   | 删除公共空间上下文             | 无                                         | 删除公共空间上下文 | 
| `sendUserDataFile`         | `sudf`   | `SendUserDataFile`        | `USERFILE`  | 4.0.2.1 Beta   | 发送用户数据文件               | 无                                         | 发送用户数据文件 |
| `changeContextBranch`      | `ccb`    | `ChangeContextBranch`     | `CONTEXT`   | 4.1.2.0        | 切换上下文分支                 | 分支名称                                   | 切换上下文分支 |
| `changePromptBranch`       | `cppb`   | `ChangePromptBranch`      | `PROMPT`    | 4.1.2.0        | 切换提示词分支                 | 分支名称                                   | 切换提示词分支 |
| `changeConfigBranch`       | `ccfgb`  | `ChangeConfigBranch`      | `CONFIG`    | 4.1.2.0        | 切换配置分支                   | 分支名称                                   | 切换配置分支 |
| `reference`                | `ref`    | `Reference`               | `CHAT`      | 4.1.2.0        | 引用上下文                     | @群成员并输入自然语言                       | 引用其他用户的上下文进行生成，并将结果保存到自己的聊天记录中 |
| `chooseGroupMember`        | `cgm`    | `ChooseGroupMember`       | `OTHER`     | 4.1.2.0        | 抽取群组成员                   | 抽取数量                                   | 抽取群组成员 |
| `withdraw`                 | `w`      | `Withdraw`                | `CONTEXT`   | 4.2.3.0        | 撤回消息                       | 无                                        | 删除复读机上下文中保存的最新一回合对话 |
| `recentSpeakingRanking`    | `rsr`    | `RecentSpeakingRanking`   | `OTHER`     | 4.2.3.0        | 最近发言排行                   | 无                                        | 获取群组内最近发言的成员列表 |
| `setAutoShrinkLength`      | `sasl`   | `SetAutoShrinkLength`     | `CONFIG`    | 4.2.4.0        | 设置自动缩减长度上限            | 目标消息字数                              | 如果你的聊天总字数超过该值，系统会尝试自动删除最旧的直到满足该值 |
| `getNamespace`             | `gns`    | `GetNamespace`            | `NAMESPACE` | 4.2.4.4        | 获取命名空间                   | @目标用户 (不填就是自己)                    | 获取当前或指定用户的命名空间 |
| `deleteSession`            | `ds`     | `DeleteSession`           | `MIXED`     | 4.2.5.0        | 删除所有用户数据               | 无                                        | 删除所有用户数据 |
| `raw`                      | `raw`    | `Raw`                     | `CHAT`      | 4.2.5.1        | 发送消息且不包含任何元数据      | 自然语言输入                               | 发送消息且不包含任何元数据 |
| `changeSession`            | `cs`     | `ChangeSession`           | `MIXED`     | 4.2.5.1        | 让所有的数据同时切换到一个分支  | 分支名称                                  | 让`Context`、`Prompt`、`Config`同时切换到一个分支 |
| `noSaveChat`               | `nsc`    | `NoSaveChat`              | `CHAT`      | 4.2.6.6        | 不保存的聊天对话              | 无                                        | 聊天后不保存最新聊天记录 |
| `summaryChatRecord`        | `scr`    | `SummaryChatRecord`       | `OTHER`     | 4.2.6.6        | 聊天记录总结                  | 整数，传入的消息数量                       | 获取当前群聊内指定数量的聊天记录摘要 |
| `varExpandText`            | `vet`    | `Var_Expand_Text`         | `VAREXPAND` | 4.2.7.0        | 变量展开(文本)                | 文本模板                                 | 强制使用文本输出 |
| `varExpandImage`           | `vei`    | `Var_Expand_Image`        | `VAREXPAND` | 4.2.7.0        | 变量展开(图片)                | 文本模板                                 | 强制使用图片输出 |
| `setAutoLoadPrompt`        | `salp`   | `SetAutoLoadPrompt`       | `CONFIG`    | 4.3.1.0        | 设置自动加载提示词            | `true`/`false`                           | 设置请求时是否自动加载Prompt |
| `setAutoSaveContext`       | `sasc`   | `SetAutoSaveContext`      | `CONFIG`    | 4.3.1.0        | 设置自动保存上下文            | `true`/`false`                           | 设置生成完毕后是否自动保存Context |
| `setRenderTitle`           | `srt`    | `SetRenderTitle`          | `CONFIG`    | 4.3.2.1        | 设置渲染标题                 | 任意文本                                   | 渲染时显示的标题内容 |
| `setTimezone`              | `stz`    | `SetTimezone`             | `CONFIG`    | 4.3.3.3        | 设置时区                     | 时区名称(如`Asia/Shanghai`)                | 请使用确定的时区名称 |
| `writeUserProfile`         | `wup`    | `WriteUserProfile`        | `CONFIG`    | 4.3.3.6        | 写入用户人设数据              | 任意文本                                   | 该部分会被嵌入到用户提示词中，告诉AI用户的基础设定 |
| `setHtmlTemplate`          | `sht`    | `SetHtmlTemplate`         | `CONFIG`    | 4.3.3.6        | 设置HTML模板                 | 预设模板名称                               | 可以用于切换Markdown渲染时使用的HTML模板 |
| `setSaveTextOnly`          | `ssto`   | `SetSaveTextOnly`         | `CONFIG`    | 4.3.6.0        | 在保存时丢弃除文本以外的内容   | `true`/`false`                           | 设为`true`可以更快速的保存与读取，但模型将无法再获取到上下文中的附加数据 |
| `textRender`               | `tr`     | `TextRender`              | `RENDER`    | 4.3.7.0        | Markdown 文本渲染            | Markdown 文本                             | 将 Markdown 文本渲染为图片 |
| `getModelList`             | `gml`    | `GetModelList`            | `MODEL`     | 4.3.7.4        | 获取模型列表                 | 模型类型(目前只有`chat`)                   | 获取模型列表 |
| `generatePrompt`           | `genp`   | `GeneratePrompt`          | `MIXED`     | 4.3.7.5        | 生成提示词                   | 角色描述                                  | 生成提示词，并自动保存到用户提示词数据中 |
| `summarizeAndContract`     | `sac`    | `SummarizeAndContract`    | `CHAT`      | 4.3.7.6        | 摘要并压缩                   | 自定义提示词，可以为空                      | 摘要并压缩对话，并自动删除多余的历史记录 |
| `contextBranchClone`       | `cbc`    | `ContextBranchClone`      | `CONTEXT`   | 4.3.9.1        | 克隆上下文分支                | 目标分支名称                               | 将当前活动分支复制到一个新的分支下 |
| `contextBranchCloneFrom`   | `cbcf`   | `ContextBranchCloneFrom`  | `CONTEXT`   | 4.3.9.1        | 从分支克隆上下文              | 源分支名称                                 | 将指定分支复制到当前活动分支下 |
| `promptBranchClone`        | `pbc`    | `PromptBranchClone`       | `PROMPT`    | 4.3.9.1        | 克隆提示词分支                | 目标分支名称                               | 将当前活动分支复制到一个新的分支下 |
| `promptBranchCloneFrom`    | `pbcf`   | `PromptBranchCloneFrom`   | `PROMPT`    | 4.3.9.1        | 从分支克隆提示词              | 源分支名称                                 | 将指定分支复制到当前活动分支下 |
| `configBranchClone`        | `cfgbc`  | `ConfigBranchClone`       | `CONFIG`    | 4.3.9.1        | 克隆配置分支                  | 目标分支名称                               | 将当前活动分支复制到一个新的分支下 |
| `configBranchCloneFrom`    | `cfgbcf` | `ConfigBranchCloneFrom`   | `CONFIG`    | 4.3.9.1        | 从分支克隆配置                | 源分支名称                                 | 将指定分支复制到当前活动分支下 |
| `contextBranchBind`        | `cbb`    | `ContextBranchBind`       | `CONTEXT`   | 4.3.9.1        | 绑定上下文分支                | 目标分支名称                               | 创建一个新的分支，使其硬链接到当前活动分支 |
| `contextBranchBindFrom`    | `cbbf`   | `ContextBranchBindFrom`   | `CONTEXT`   | 4.3.9.1        | 从分支绑定上下文              | 源分支名称                                 | 删除当前活动分支的内容，并作为指定分支的硬链接 |
| `promptBranchBind`         | `pbb`    | `PromptBranchBind`        | `PROMPT`    | 4.3.9.1        | 绑定提示词分支                | 目标分支名称                               | 创建一个新的分支，使其硬链接到当前活动分支 |
| `promptBranchBindFrom`     | `pbbf`   | `PromptBranchBindFrom`    | `PROMPT`    | 4.3.9.1        | 从分支绑定提示词              | 源分支名称                                 | 删除当前活动分支的内容，并作为指定分支的硬链接 |
| `configBranchBind`         | `cfgbb`  | `ConfigBranchBind`        | `CONFIG`    | 4.3.9.1        | 绑定配置分支                  | 目标分支名称                               | 创建一个新的分支，使其硬链接到当前活动分支 |
| `configBranchBindFrom`     | `cfgbbf` | `ConfigBranchBindFrom`    | `CONFIG`    | 4.3.9.1        | 从分支绑定配置                | 源分支名称                                 | 删除当前活动分支的内容，并作为指定分支的硬链接 |
| `contextBranchInfo`        | `cbi`    | `ContextBranchInfo`       | `CONTEXT`   | 4.3.9.1        | 获取分支元数据信息            | 无                                         | 获取当前活动分支的元数据信息 |
| `promptBranchInfo`         | `pbi`    | `PromptBranchInfo`        | `PROMPT`    | 4.3.9.1        | 获取分支元数据信息            | 无                                         | 获取当前活动分支的元数据信息 |
| `configBranchInfo`         | `cfgbi`  | `ConfigBranchInfo`        | `CONFIG`    | 4.3.9.1        | 获取分支元数据信息            | 无                                         | 获取当前活动分支的元数据信息 |
| `sessionBranchClone`       | `sbc`    | `SessionBranchClone`      | `MIXED`     | 4.3.9.3        | 克隆所有类型分支              | 目标分支名称                                | 将所有类型的当前活动分支复制到一个新的分支下 |
| `sessionBranchCloneFrom`   | `sbcf`   | `SessionBranchCloneFrom`  | `MIXED`     | 4.3.9.3        | 所有类型从指定分支克隆        | 源分支名称                                  | 所有类型的当前活动分支从指定分支复制 |
| `sessionBranchBind`        | `sbb`    | `SessionBranchBind`       | `MIXED`     | 4.3.9.3        | 所有类型绑定指定分支          | 目标分支名称                                | 所有类型同时创建一个新分支，硬链接到当前活动分支 |
| `sessionBranchBindFrom`    | `sbbf`   | `SessionBranchBindFrom`   | `MIXED`     | 4.3.9.3        | 所有类型绑定指定分支          | 源分支名称                                  | 所有类型同时删除活动分支数据，并从指定分支硬链接一份活动分支文件 |
| `#` or `/`                 | `anot`   | `Annotation`              | `RESERVED`  | 4.3.9.3        | 注释，不会执行任何操作        | 无                                         | 不执行任何操作，直接忽略内容，由于命令前缀的存在，触发需要 `/#` 或 `//` |
| `crossUserDataAccess`      | `cuda`   | `CrossUserDataAccess`     | `CONFIG`    | 4.3.10.3       | 允许跨用户数据访问            | `true`/`false`                            | 允许跨用户数据访问，如果设置为`false`则只能访问自己的数据 |
| `newRequestsTextOnly`      | `nrto`   | `NewRequestsTextOnly`     | `CONFIG`    | 4.3.10.7       | 忽略请求里的非文本数据        | `true`/`false`                            | 如果设置为`true`，复读机将把所有消息当成普通文本消息处理 |
| `adaptationInfo`           | `adai`   | `AdaptationInfo`          | `VERSION`   | 4.3.10.7       | 版本适配信息                 | 无                                         | 展示服务端和客户端的版本信息 |
| `getRequirementLicenses`   | `grl`    | `GetRequirementLicenses`  | `LICENSES`  | 4.3.10.8       | 获取依赖许可证               | 依赖项名称                                  | 获取指定依赖的许可证信息 |
| `getRequirementList`       | `grls`   | `GetRequirementList`      | `LICENSES`  | 4.3.10.8       | 获取依赖列表                 | 无                                         | 获取所有记录了License的依赖项名称 |
| `getServerLicense`         | `gsl`    | `GetServerLicense`        | `LICENSES`  | 4.3.10.8       | 获取服务端许可证             | 无                                         | 获取服务端许可证信息 |
| `checkRoleStructure`       | `crs`    | `CheckRoleStructure`      | `CONTEXT`   | 4.3.10.10      | 检查角色结构                 | 无                                        | 检查上下文中的角色结构是否符合 user-assistant 的规则 |
| `contextUploadToNexus`     | `cutn`   | `ContextUploadToNexus`    | `NEXUS`     | 4.3.11.0       | 上传上下文到 Nexus           | 超时秒数                                   | 上传上下文到Nexus共享 |
| `contextDownloadFromNexus` | `cdfn`   | `ContextDownloadFromNexus`| `NEXUS`     | 4.3.11.0       | 从 Nexus 下载上下文          | 资源 UUID                                 | 下载Nexus共享的上下文 |
| `promptUploadToNexus`      | `putn`   | `PromptUploadToNexus`     | `NEXUS`     | 4.3.11.0       | 上传提示词到 Nexus           | 超时秒数                                   | 上传提示词到Nexus共享 |
| `promptDownloadFromNexus`  | `pgetn`  | `PromptDownloadFromNexus` | `NEXUS`     | 4.3.11.0       | 从 Nexus 下载提示词          | 资源 UUID                                 | 获取Nexus共享的提示词 |
| `configUploadToNexus`      | `cfgutn` | `ConfigUploadToNexus`     | `NEXUS`     | 4.3.11.0       | 上传配置到 Nexus             | 超时秒数                                  | 个性配置上传到Nexus |
| `configDownloadFromNexus`  | `cfgdtn` | `ConfigDownloadFromNexus` | `NEXUS`     | 4.3.11.0       | 从 Nexus 下载配置            | 资源 UUID                                 | 从Nexus下载共享的个性配置 |
| `setCustomName`            | `scn`    | `SetCustomName`           | `CONFIG`    | 4.3.12.1       | 设置个性化名称               | 用户名                                    | 设置后模型看到的将是设置的名称而非用户名 |
| `thinkingMode`             | `tm`     | `ThinkingMode`            | `CONFIG`    | 4.3.14.0       | 设置思考模式                 | `true`/`false`/`null`                    | 用于在不指定 Thinking 参数时 启用/禁用/恢复默认 思考模式 |
| `noReason`                 | `nr`     | `NoReason`                | `CHAT`      | 4.3.15.0       | 不使用 Thinking 进行对话     | 自然语言输入                              | 关闭 `thinking` 参数以阻止进入 Thinking 模式 |
| `noPromptEcho`             | `npecho` | `NoPromptEcho`            | `ECHO`      | 4.3.16.0       | 无额外反应的 Echo            | 任何内容                                  | 与 `echo` 命令相同，但不在未找到参数时显示等待提示词 |
| `getContextBranchsList`    | `gcbl`   | `GetContextBranchslist`   | `CONTEXT`   | 4.3.16.7       | 获取分支列表                 | 无                                        | 返回当前用户的上下文分支列表 |
| `getPromptBranchList`      | `gpbl`   | `GetPromptBranchList`     | `PROMPT`    | 4.3.16.7       | 获取提示词分支列表           | 无                                        | 返回当前用户的提示词分支列表 |
| `getConfigBranchList`      | `gcfgbl` | `GetConfigBranchList`     | `CONFIG`    | 4.3.16.7       | 获取当前上下文分支           | 无                                        | 获取当前上下文分支 |
| `getCoreTaskStatus`        | `gcts`   | `GetCoreTaskStatus`       | `STATUS`    | 4.3.17.0       | 获取当前任务状态             | 无                                        | 获取当前核心任务状态 (Free or Task Stack) |
| `generateCandidateAnswer`  | `gca`    | `GenerateCandidateAnswer` | `CHAT`      | 4.3.18.0       | 生成候选答案                 | 无                                        | 生成候选答案（生成内容不保存） |
| `envUploadToNexus`         | `eutn`   | `EnvUploadToNexus`        | `NEXUS`     | 4.3.19.0       | 上传环境到 Nexus             | 超时秒数                                  | 同时上传所有用户数据到Nexus |
| `envDownloadFromNexus`     | `edfn`   | `EnvDownloadFromNexus`    | `NEXUS`     | 4.3.19.0       | 从 Nexus 下载环境            | 资源 UUID                                 | 从 Nexus 同时下载所有用户数据 |
| `generateCandidateReason`  | `gcr`    | `GenerateCandidateReason` | `CHAT`      | 4.3.23.1       | 生成候选推理                 | 无                                        | 生成候选回答并开启推理（生成内容不保存） |
| `setModelTimeout`          | `smto`   | `SetModelTimeout`         | `CONFIG`    | 4.3.25.0       | 设置模型超时时间             | 超时秒数                                   | 设置模型超时时间 |
| `removeReasoningPrompt`    | `rrp`    | `RemoveReasoningPrompt`   | `CONFIG`    | 4.3.26.0       | 删除推理内容                 | 删除推理内容 |                             | 设置是否在提交时移除模型输出的思考内容（不影响保存） |
| `breakChatTask`            | `bct`    | `BreakChatTask`           | `STATUS`    | 4.4.4.0        | 中止当前所有生成任务         | 无                                         | 中止当前所有生成任务，中止后模型已生成内容将不会保存和显示 |
| `renderDocBottomComment`   | `rdbc`   | `RenderDocBottomComment`  | `CONFIG`    | 4.4.4.0        | 渲染文档底部注释             | 文本内容                                   | 在渲染图片的底部添加一小段文本 |
| `calculateLengthScore`     | `cls`    | `CalculateLengthScore`    | `OTHER`     | 4.4.4.0        | 计算长度评分                 | 文本内容                                   | 计算给定文本的长度评分值 |
| `fastStatisticsTemplate`   | `fst`    | `FastStatisticsTemplate`  | `CONFIG`    | 4.4.5.0        | 快速统计模板                 | 模板内容                                   | 可以在生成的图片结尾展示一些统计数据 |
| `setMultipleModel`         | `smm`    | `SetMultipleModel`        | `CONFIG`    | 4.4.6.0        | 设置多个模型                 | *多个模型名称*                              | 设置多个模型，当访问时随机选择一个模型 |
| `setStopKeywords`          | `ssk`    | `SetStopKeywords`         | `CONFIG`    | 4.4.6.0        | 设置停止关键词               | *多个停止关键词*                            | 当模型生成出这个词时，暂停模型生成并即刻返回结果 |
| `injectUserContent`        | `iuc`    | `InjectUserContent`       | `CONTEXT`   | 4.4.7.0        | 注入用户消息内容             | 消息内容                                   | 插入用户消息内容 |
| `injectAssistantContent`   | `iac`    | `InjectAssistantContent`  | `CONTEXT`   | 4.4.7.0        | 插入 AI 消息内容             | 消息内容                                   | 插入 AI 消息内容 |
| `injectSystemContent`      | `isc`    | `InjectSystemContent`     | `CONTEXT`   | 4.4.7.0        | 插入系统消息内容             | 消息内容                                   | 插入系统消息内容 |
| `getChatBuffer`            | `gcb`    | `GetChatBuffer`           | `STATUS`    | 4.4.8.0        | 获取聊天缓冲区               | 无                                        | 获取当前会话的聊天缓冲区 |
| `getLastContent`           | `glc`    | `GetLastContent`          | `CONTEXT`   | 4.4.8.0        | 获取最后一条消息内容          | 无                                        | 获取当前会话的最后一条消息内容 |
| `getConfig`                | `gcfg`   | `GetConfig`               | `CONFIG`    | 4.4.8.0        | 获取配置                     | `JSON`/`YAML`                             | 获取当前会话的配置 |
| `getPrompt`                | `gp`     | `GetPrompt`               | `PROMPT`    | 4.4.8.0        | 获取提示词                   | 无                                        | 获取当前会话的提示词 |
| `setCustomAge`             | `sca`    | `SetCustomAge`            | `CONFIG`    | 4.4.9.0        | 设置自定义年龄               | 年龄                                       | 设置自定义年龄 (需要提示词支持) |
| `setCustomGender`          | `scg`    | `SetCustomGender`         | `CONFIG`    | 4.4.9.0        | 设置自定义性别               | 性别                                       | 设置自定义性别 (需要提示词支持) |
| `sendMessage`              | `smsg`   | `SendMessage`             | `SENDMSG`   | 4.4.12.0       | 发送消息                    | OneBot 消息结构                             | 发送一条自定义消息（需要 `allow_send_any_message` 字段为 `true`） |
| `singleWithdraw`           | `sw`     | `SingleWithdraw`          | `CONTEXT`   | 4.4.13.0       | 单条撤回                    | 消息条数                                    | 直接按条撤回消息（而不是按对撤回） |
| `sendContextFile`          | `scf`    | `SendContextFile`         | `CONTEXT`   | 4.5.5.0-beta   | 发送聊天记录文件             | 无                                          | 获取当前活动分支的聊天记录文件 |
| `sendPromptFile`           | `spf`    | `SendPromptFile`          | `PROMPT`    | 4.5.5.0-beta   | 获取提示词文件               | 无                                          | 获取当前活动分支的提示词文件 |
| `sendConfigFile`           | `scfgf`  | `SendConfigFile`          | `CONFIG`    | 4.5.5.0-beta   | 获取配置文件                 | 无                                          | 获取当前活动分支的配置文件 |
| `packageUserSpace`         | `pus`    | `PackageUserSpace`        | `USERFILE`  | 4.5.5.0        | 打包用户空间                 | 无                                          | 与 `sendUserDataFile` 类似，但它会打包所有分支 |
| `setReasoningEffort`       | `sre`    | `SetReasoningEffort`      | `CONFIG`    | 4.5.6.0        | 设置推理强度                 | `low`/`medium`/`high`/`xhigh`/`max`         | 设置推理强度 (需要模型支持) |
| `resetConfigField`         | `rcf`    | `ResetConfigField`        | `CONFIG`    | 4.5.6.0        | 重置配置字段                 | 配置字段名称                                 | 设置指定配置字段到 null |
| `makeMultimodalMessage`    | `mmm`    | `MakeMultimodalMessage`   | `CONFIG`    | 4.5.8.0        | 是否创建多模态消息            | `true`/`false`                              | 设置是否创建多模态消息 |
| `allowedToolCalls`         | `atc`    | `AllowedToolCalls`        | `CONFIG`    | 4.5.8.0        | 批准使用工具                 | *\*多个工具注册名*                           | 指定 AI 能使用哪些工具 |

PS：`CHAT`类型命令大部分都做到了支持视觉输入
默认命令已支持全模态输入
为了速度和减少本机网络开销，复读机会直接使用QQ传递的临时URL
你可以在配置中改用 Base64 编码的 URL
(这只对图片数据有效)
但想要 Repeater Server 不忽略附加数据需要主动设置 `NewRequestsTextOnly` 为 `false`
或是找管理员关闭 Repeater Server 的自动拦截

`MIXED`类型命令是混合型命令
它的一条命令会执行多条后端请求
通常，它会从基础功能拼接出高级功能
或是同时操作多个数据内容

`NEXUS` 系列命令操作的是当前活动分支
所以在下载前请确保你的活动分支上没有重要数据

当命令需要传入多个参数时
参数需要通过指定分隔符进行拆分
支持的分隔符为 `|`, `,`, `;`, `/`, `\n`
分割时会按照最先出现的一个分隔符开始分割
即使后面出现了其他分隔符，也会作为子字符串的一部分
而不是也当成分隔符去切割子字符串

所有命令都有变体
多单词的命令格式有：

- `lowerCamelCase`
- `UpperCamelCase`
- `snake_case`
- `Upper_Snake_Case`
- `UPPER_CASE`
- `abr` (Abridge)
- `ABR` (UPPER ABRIDGE)

而单个单词的命令有些特殊：

- `lowercase`
- `Uppercase`
- `s` (Single Character)
- `S` (UPPER SINGLE CHARACTER)
- `slbc` (Syllabic abbreviations)
- `SLBC` (UPPER SYLLABIC ABBREVIATIONS)

通常来说，如果一个新命令
缩写与旧命令有冲突
则尽量保持旧命令不变
除非它是基础级别的命令

---

## 相关仓库
- [Repeater Server](https://github.com/qeggs-dev/repeater-ai-chatbot)