# ChatGPT Telegram機器人

加入[Telegram群組](https://t.me/+_01cz9tAkUc1YzZl)聊天以分享您的用戶體驗或報告錯誤。

[英語](./README.md) | [簡體中文](./README.zh-CN.md) | [繁體中文](./README.zh-TW.md)

## ✨ 功能

✅ 支持ChatGPT和GPT4 API

✅ 支持使用duckduckgo和Google🔍進行在線搜索。默認情況下提供DuckDuckGo搜索，而使用Google搜索的官方API需要用戶申請。它可以提供GPT無法在過去回答的實時信息，例如今日微博熱門搜索，某個地方的天氣和某個人或新聞的進度等。

✅ 基於嵌入式向量數據庫支持文檔QA。在搜索中，對於搜索的PDF，執行PDF文檔的自動向量語義搜索，並基於向量數據庫提取與pdf相關的內容。支持使用“qa”命令使用“sitemap.xml”文件將整個網站向量化，並基於向量數據庫回答問題，尤其適用於一些項目的文檔網站和Wiki網站。

✅ 支持通過聊天窗口中的“info”命令在GPT3.5，GPT4和其他模型之間切換

✅ 異步處理消息，多線程回答問題，支持隔離對話，不同的用戶擁有不同的對話

✅ 支持消息的準確的Markdown渲染，使用我另一個 [project](https://github.com/yym68686/md2tgmd)

✅ 支持流式輸出，實現打字機效果

✅ 支持白名單警戒，防止濫用和信息洩露

✅ 跨平臺，隨時隨地在Telegram上突破知識障礙

✅ 支持一鍵Zeabur，Replit部署，真正的零成本易用部署，支持kuma防睡眠。還支持Docker，fly.io部署

## 環境變量

| 變量名              | 評論                                                         |
| ------------------- | ------------------------------------------------------------ |
| **BOT_TOKEN（必填）** | Telegram機器人令牌。在[BotFather](https://t.me/BotFather)上創建一個機器人，即可獲得BOT_TOKEN。 |
| **WEB_HOOK（必填）**  | 當Telegram機器人接收到用戶消息時，消息將被傳遞到WEB_HOOK，機器人將在此處聽取消息並及時處理接收到的消息。|
| **API（必填）**       | OpenAI或第三方API密鑰。                                   |
| API_URL（可選）       | 如果您使用的是OpenAI 的官方API，则不需要設置此設置。如果使用第三方API，則需要填寫第三方代理網站。默認值為：https://api.openai.com/v1/chat/completions |
| GPT_ENGINE（可選）    | 設置默認的QA模型;默認值為：`gpt-3.5-turbo`。該項目可以通過機器人的“info”命令自由切換，原則上不需要設置。 |
| NICK（可選）          | 默認值為空，而NICK是機器人的名字。只有當用戶輸入的消息以NICK開始時，機器人才會響應，否則機器人將響應任何消息。特別是在群聊中，如果沒有NICK，機器人將回復所有消息。 |
| PASS_HISTORY（可選）  | 默認值為true。機器人記住對話歷史記錄，並在下次回復時考慮上下文。如果設置為false，機器人將忘記對話歷史記錄，僅考慮當前對話。 |
| GOOGLE_API_KEY（可選）| 如果您需要使用Google搜索，則需要進行設置。如果不設置此環境變量，機器人將默認提供duckduckgo搜索。在Google Cloud的APIs＆Services中創建憑據（https://console.cloud.google.com/apis/api/customsearch.googleapis.com），並在凭据页面上点选API密钥。Google搜索每天可以查詢100次，这完全足够轻度使用。当达到使用限制时，机器人将自动关闭Google搜索。 |
| GOOGLE_CSE_ID（可選） | 如果您需要使用Google搜索，則必須與GOOGLE_API_KEY一起設置。在[Programmable Search Engine](https://programmablesearchengine.google.com/)中創建搜索引擎，搜索引擎ID即为GOOGLE_CSE_ID的值。 |
| 白名單（可選）      | 設置哪些用戶可以訪問機器人，將被授權使用機器人的用戶ID與“,”相連。默認值為`None`，這意味着所有人都可以使用機器人。 |

## Zeabur遠程部署(推薦)

一鍵部署：

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686)

如果您需要後續功能更新，建議使用以下部署方法：

先Fork本存儲庫，然後註冊[Zeabur](https://zeabur.com)。免費配額足以輕度使用。從您自己的Github存儲庫導入，設置域名（必須與WEB_HOOK一致）和環境變量，然後重新部署。如果需要在後續升級時，只需要在自己的存儲庫中同步這個存儲庫，然後重新部署即可獲得最新的功能。

## Replit遠程部署

[![Run on Repl.it](https://replit.com/badge/github/yym68686/ChatGPT-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Telegram-Bot)

匯入Github存儲庫後，設置運行命令

```bash
pip install -r requirements.txt > /dev/null && python3 main.py
```

在工具側邊欄中選擇Secrets，添加機器人需要的環境變量，其中：

- WEB_HOOK：Replit会自动为您分配一个域名，填写“https://appname.username.repl.co”
- 記得開啟“始終開啟”

單擊屏幕頂部的運行按鈕以運行機器人。

## fly.io遠程部署

官方文檔： https://fly.io/docs/

使用Docker映像部署fly.io應用程序

```bash
flyctl launch --image yym68686/chatgpt:1.0
```

輸入應用程序名字，並選擇否初始化Postgresql或Redis。

按照提示部署。官方控制面板提供了辅助域名，可用于访问服务。

設置環境變量

```bash
flyctl secrets set WEB_HOOK=https://flyio-app-name.fly.dev/
flyctl secrets set BOT_TOKEN=bottoken
flyctl secrets set API=
# optional
flyctl secrets set NICK=javis
```

查看所有環境變量

```bash
flyctl secrets list
```

刪除環境變量

```bash
flyctl secrets unset MY_SECRET DATABASE_URL
```

ssh到fly.io容器

```bash
flyctl ssh issue --agent
# ssh connection
flyctl ssh establish
```

檢查webhook URL是否正確

```bash
https://api.telegram.org/bot<token>/getWebhookInfo
```

## Docker本地部署

啟動容器

```bash
docker run -p 80:8080 -dit \
    -e BOT_TOKEN="telegram bot token" \
    -e WEB_HOOK="https://your_host.com/" \
    -e API="" \
    -e API_URL= \
    yym68686/chatgpt:1.0
```

或者，如果您想要使用Docker Compose，這是一個docker-compose.yml示例：

```yaml
version: "3.5"
services:
  chatgptbot:
    container_name: chatgptbot
    image: yym68686/chatgpt:1.0
    environment:
      - BOT_TOKEN=
      - WEB_HOOK=
      - API=
      - API_URL=
    ports:
      - 80:8080
```

在背景中運行Docker Compose容器

```bash
docker-compose up -d
```

在存储库中打包Docker映像并将其上载到Docker Hub

```bash
docker build --no-cache -t chatgpt:1.0 -f Dockerfile.build --platform linux/amd64 .
docker tag chatgpt:1.0 yym68686/chatgpt:1.0
docker push yym68686/chatgpt:1.0
```

## 參考文獻

參考項目：

https://core.telegram.org/bots/api

https://github.com/acheong08/ChatGPT

https://github.com/franalgaba/chatgpt-telegram-bot-serverless

https://github.com/gpchelkin/scdlbot/blob/d64d14f6c6d357ba818e80b8a0a9291c2146d6fe/scdlbot/__main__.py#L8

消息的Markdown渲染使用的是我另一個 [project](https://github.com/yym68686/md2tgmd)

## 星等历史

<a href="https://github.com/yym68686/ChatGPT-Telegram-Bot/stargazers">
        <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=yym68686/ChatGPT-Telegram-Bot&type=Date">
</a>