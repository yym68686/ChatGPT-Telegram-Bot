# ChatGPT Telegram Bot

加入 [Telegram 群聊](https://t.me/+_01cz9tAkUc1YzZl) ，分享您的用戶體驗或報告錯誤。

[英文](./README.md) | [簡體中文](./README.zh-CN.md) | [繁體中文](./README.zh-TW.md)

## ✨ 功能

✅ 支援 ChatGPT 和 GPT4 API

✅ 支持使用 duckduckgo 和 Google🔍 的在線搜尋。DuckDuckGo 搜尋默認提供，使用者需要申請官方的 Google 搜尋 API，它可以提供 GPT 之前無法回答的實時信息，例如今日微博熱搜、某地天氣、某人或新聞的進展等。

✅ 支援基於嵌入式向量數據庫的文件 QA。在搜尋中，搜索到的 PDF 會自動進行 PDF 文件的向量語義搜索，並根據向量數據庫提取相關內容。支持使用“qa”命令將“sitemap.xml”文件的整個網站向量化，並基於向量數據庫回答問題，特別適用於一些項目的文檔網站和 Wiki 網站。

✅ 在聊天窗口中通過“info”命令支援在 GPT3.5、GPT4 和其他模型之間進行切換

✅ 異步處理消息，多線程回答問題，支援隔離對話，不同用戶有不同對話

✅ 支援消息的精確的 Markdown 渲染，使用我另一個項目 [project](https://github.com/yym68686/md2tgmd) 

✅ 支援流式輸出，實現打字機效果

✅ 支援白名單，防止濫用和信息外洩

✅ 跨平台，在 Telegram 上隨時隨地打破知識壁壘

✅ 支援一鍵 Zeabur，Replit 部署，真正的零成本，傻瓜式部署，還支援 kuma 防睡眠。也支援 Docker、fly.io 部署

## 環境變數

| 變量名稱                  | 評論                                                         |
| ------------------------- | ------------------------------------------------------------ |
| **BOT_TOKEN (必需的)**    | Telegram 機器人 token。在 [BotFather](https://t.me/BotFather) 上創建一個機器人來獲取 BOT_TOKEN。 |
| **WEB_HOOK (必需的)**     | 當 Telegram 機器人收到用戶信息時，該信息將被傳遞到 WEB_HOOK，機器人將在 WEB_HOOK 上聽取並及時處理接收到的消息。 |
| **API (必需的)**          | OpenAI 或第三方 API 憑證。                                 |
| API_URL(可選)             | 如果使用的是 OpenAI 官方 API，則不需要設置此值，如果使用第三方 API，則需要填寫第三方代理網站。默認為：https://api.openai.com/v1/chat/completions |
| GPT_ENGINE (可選)         | 設置默認 QA 模型；默認為 `gpt-3.5-turbo`。此項目可以在機器人的“info”命令中自由切換，理論上不需要設置。 |
| NICK(可選)                |  默認值為空，NICK 是機器人的名字。只有當用戶輸入內容以 NICK 開頭時，機器人才會回覆，否則機器人會回覆任何消息。特別是在群聊中，如果沒有"NICK"，機器人會回覆所有消息。 |
| PASS_HISTORY(可選)        | 默認為 true。機器人會記住對話歷史，並在下次回覆時考慮上下文。如果設置為 false，則機器人將忘記對話記錄，僅考慮當前對話。 |
| GOOGLE_API_KEY(可選)      | 如果需要使用 Google 搜尋，則需要設置它。如果未設置此環境變量，機器人將默認提供 duckduckgo 搜尋。在 Google Cloud 的 [API 及服務](https://console.cloud.google.com/apis/api/customsearch.googleapis.com) 中創建憑證，API 金鑰將在憑證頁面上的 GOOGLE_API_KEY 中。Google 搜尋可以查詢100次/天，對於輕度使用來說完全足夠。當使用限制已達到時，機器人將自動關閉 Google 搜尋。 |
| GOOGLE_CSE_ID(可選)       | 如果需要使用 Google 搜尋，則需要與 GOOGLE_API_KEY 一起設置。在 [可編程搜索引擎](https://programmablesearchengine.google.com/) 中創建搜索引擎，搜索引擎 ID 是 GOOGLE_CSE_ID 的值。 |
| whitelist(可選)          | 設置哪些用戶可以訪問機器人，並將使用機器人的授權用戶 ID 連接起來，用“,”隔開。默認值為“None”，這意味著機器人向所有人開放。 |

## Zeabur 遠程部署（建議）

單擊一鍵部署：

[![在 Zeabur 上部署](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686)

如果需要後續功能更新，建議採用以下部署方法：

首先，先 fork 此存儲庫，然後註冊 [Zeabur](https://zeabur.com)。免費配額對於輕度使用來說足夠了。從您自己的 Github 存儲庫導入，設置域名（必須與 WEB_HOOK 一致）和環境變量，然後重新部署。如果需要更新後續功能，只需同步此存儲庫到自己的存儲庫中，然後在 Zeabur 中重新部署以獲取最新的功能。

## Replit 遠程部署

[![在 Repl.it 上運行](https://replit.com/badge/github/yym68686/ChatGPT-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Telegram-Bot)

匯入 Github 存儲庫後，設置運行命令

```bash
pip install -r requirements.txt > /dev/null && python3 main.py
```

在工具邊欄中選擇 Secrets，添加機器人所需的環境變量：

- WEB_HOOK：Replit將自動分配域名給您，填寫 `https://appname.username.repl.co`
- 記住打開“一直開啟”。

單擊屏幕頂部的運行按鈕以運行機器人。

## fly.io 遠程部署

官方文檔: https://fly.io/docs/

使用 Docker 映像部署 fly.io 應用

```bash
flyctl launch --image yym68686/chatgpt:1.0
```

在提示時輸入應用程序名稱，然後對初始化 Postgresql 或 Redis 選擇“不”。按照提示部署。一個二級域名將在官方控制面板中提供，可用於訪問服務。

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

ssh 到 fly.io 容器

```bash
flyctl ssh issue --agent
# ssh connection
flyctl ssh establish
```

檢查 webhook URL 是否正確

```bash
https://api.telegram.org/bot<token>/getWebhookInfo
```

## Docker 本地部署

啟動容器

```bash
docker run -p 80:8080 -dit \
    -e BOT_TOKEN="telegram bot token" \
    -e WEB_HOOK="https://your_host.com/" \
    -e API="" \
    -e API_URL= \
    yym68686/chatgpt:1.0
```

或者如果想使用 Docker Compose，此處提供一個docker-compose.yml示例：

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

在後台運行 Docker Compose 容器

```bash
docker-compose up -d
```

在存儲庫中打包 Docker 映像，並上傳至 Docker Hub：

```bash
docker build --no-cache -t chatgpt:1.0 -f Dockerfile.build --platform linux/amd64 .
docker tag chatgpt:1.0 yym68686/chatgpt:1.0
docker push yym68686/chatgpt:1.0
```

## 引用

參考項目：

https://core.telegram.org/bots/api

https://github.com/acheong08/ChatGPT

https://github.com/franalgaba/chatgpt-telegram-bot-serverless

https://github.com/gpchelkin/scdlbot/blob/d64d14f6c6d357ba818e80b8a0a9291c2146d6fe/scdlbot/__main__.py#L8

消息的 markdown 渲染使用我的另一個項目 [project](https://github.com/yym68686/md2tgmd)。

## Star History

<a href="https://github.com/yym68686/ChatGPT-Telegram-Bot/stargazers">
        <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=yym68686/ChatGPT-Telegram-Bot&type=Date">
</a>