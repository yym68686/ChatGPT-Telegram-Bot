# ChatGPT Telegram Bot

加入 [Telegram 群組](https://t.me/+_01cz9tAkUc1YzZl) 聊天，分享您的使用體驗或回報錯誤。

[English](./README.md) | [簡體中文](./README.zh-CN.md) | [繁體中文](./README.zh-TW.md)

## ✨ 功能

✅ 支援 ChatGPT 和 GPT4 API

✅ 支援使用 duckduckgo 和 Google🔍 進行線上搜尋。預設提供 duckduckgo 搜尋，如需使用 Google 搜尋，需由使用者申請官方 API。可以提供 GPT 以前無法回答的即時資訊，例如今日微博熱搜、某地今日天氣、某人或新聞的進展等。

✅ 支援基於嵌入向量資料庫的文件 QA。在搜尋中，對搜尋到的 PDF 進行自動向量語意搜尋，並根據向量資料庫提取與 PDF 相關的內容。支援使用 "qa" 命令對整個網站進行向量化處理，使用 "sitemap.xml" 文件，並根據向量資料庫回答問題，特別適用於某些專案的文件網站和 Wiki 網站。

✅ 支援在聊天窗口中通過 "info" 命令在 GPT3.5、GPT4 和其他模型之間切換

✅ 異步處理消息，多線程回答問題，支援獨立對話，不同用戶有不同的對話

✅ 支援對消息進行精確的 Markdown 渲染，使用我另一個項目的 [project](https://github.com/yym68686/md2tgmd)

✅ 支援流式輸出，實現打字機效果

✅ 支援白名單功能，防止濫用和信息外洩

✅ 跨平台，隨時隨地打破知識障礙，使用 Telegram

✅ 支援一鍵 Zeabur、Replit 部署，真正的零成本，白癡化部署，支援 kuma 防睡眠。也支援 Docker、fly.io 部署

## 環境變量

| 變量名稱                | 註解                                                         |
| ---------------------- | ------------------------------------------------------------ |
| **BOT_TOKEN (必填)**    | Telegram 機器人令牌。在 [BotFather](https://t.me/BotFather) 上創建一個機器人以獲取 BOT_TOKEN。 |
| **WEB_HOOK (必填)**     | 每當 Telegram 機器人收到用戶消息時，消息將傳遞到 WEB_HOOK，機器人將在 WEB_HOOK 監聽並及時處理收到的消息。 |
| **API (必填)**         | OpenAI 或第三方 API 金鑰。                                   |
| API_URL(可選)           | 如果您使用的是 OpenAI 官方 API，則無需設置此項。如果您使用的是第三方 API，則需要填寫第三方代理網站。默認值為：https://api.openai.com/v1/chat/completions |
| GPT_ENGINE(可選)        | 設置默認的 QA 模型；默認為：`gpt-3.5-turbo`。可以使用機器人的 "info" 命令自由切換此項，原則上不需要設置。 |
| NICK(可選)              | 默認為空，NICK 是機器人的名字。當用戶輸入的消息以 NICK 開頭時，機器人只會回應該消息，否則機器人將回應任何消息。尤其在群組聊天中，如果沒有 NICK，機器人將回復所有消息。 |
| PASS_HISTORY(可選)      | 默認為 true。機器人記住對話歷史並在下次回復時考慮上下文。如果設置為 false，機器人將忘記對話歷史，僅考慮當前對話。 |
| GOOGLE_API_KEY(可選)    | 如果需要使用 Google 搜尋，則需要設置。如果不設置此環境變量，機器人將默認提供 duckduckgo 搜尋。在 Google Cloud 的 [APIs & Services](https://console.cloud.google.com/apis/api/customsearch.googleapis.com) 中創建憑證，API 金鑰將是憑證頁面上的 GOOGLE_API_KEY。Google 搜尋每天可以查詢 100 次，對於輕度使用完全足夠。當使用限制已達到時，機器人將自動關閉 Google 搜尋。 |
| GOOGLE_CSE_ID(可選)     | 如果需要使用 Google 搜尋，則需要與 GOOGLE_API_KEY 一起設置。在 [Programmable Search Engine](https://programmablesearchengine.google.com/) 中創建搜索引擎，搜索引擎 ID 是 GOOGLE_CSE_ID 的值。 |
| whitelist(可選)        | 設置哪些用戶可以訪問機器人，將可使用機器人的授權用戶 ID 連接起來，用 ',' 分隔。默認值為 `None`，表示機器人對所有人開放。 |

## Zeabur 遠程部署（推薦）

一鍵部署：

[![Deploy on Zeabur](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686)

如果您需要後續的功能更新，建議使用以下部署方式：

首先 fork 此存儲庫，然後註冊 [Zeabur](https://zeabur.com)。免費配額對於輕度使用足夠。從您自己的 Github 存儲庫導入，設置域名（必須與 WEB_HOOK 一致）和環境變量，然後重新部署。如果需要後續的功能更新，只需在自己的存儲庫中同步此存儲庫，然後在 Zeabur 中重新部署以獲取最新的功能。

## Replit 遠程部署

[![Run on Repl.it](https://replit.com/badge/github/yym68686/ChatGPT-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Telegram-Bot)

導入 Github 存儲庫後，設置運行命令

```bash
pip install -r requirements.txt > /dev/null && python3 main.py
```

在 Tools 側邊欄中選擇 Secrets，添加機器人所需的環境變量，其中：

- WEB_HOOK：Replit 將自動為您分配一個域名，填寫 `https://appname.username.repl.co`
- 記得打開 "Always On"

點擊屏幕頂部的運行按鈕運行機器人。

## fly.io 遠程部署

官方文檔：https://fly.io/docs/

使用 Docker 鏡像部署 fly.io 應用程序

```bash
flyctl launch --image yym68686/chatgpt:1.0
```

在提示時輸入應用程序的名稱，並選擇 No 來初始化 Postgresql 或 Redis。

按照提示進行部署。官方控制面板將提供次級域名，可用於訪問服務。

設置環境變量

```bash
flyctl secrets set WEB_HOOK=https://flyio-app-name.fly.dev/
flyctl secrets set BOT_TOKEN=bottoken
flyctl secrets set API=
# 可選
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
# ssh 連接
flyctl ssh establish
```

檢查 Webhook URL 是否正確

```bash
https://api.telegram.org/bot<token>/getWebhookInfo
```

## Docker 本地部署

啟動容器

```bash
docker run -p 80:8080 --name chatbot -dit \
    -e BOT_TOKEN="telegram bot token" \
    -e WEB_HOOK="https://your_host.com/" \
    -e API="" \
    -e API_URL= \
    yym68686/chatgpt:1.0
```

或者，如果您想使用 Docker Compose，這是一個 docker-compose.yml 的示例：

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

在存儲庫中打包 Docker 鏡像並上傳到 Docker Hub

```bash
docker build --no-cache -t chatgpt:1.0 -f Dockerfile.build --platform linux/amd64 .
docker tag chatgpt:1.0 yym68686/chatgpt:1.0
docker push yym68686/chatgpt:1.0
```

## 參考

https://core.telegram.org/bots/api

https://github.com/acheong08/ChatGPT

https://github.com/franalgaba/chatgpt-telegram-bot-serverless

https://github.com/gpchelkin/scdlbot/blob/d64d14f6c6d357ba818e80b8a0a9291c2146d6fe/scdlbot/__main__.py#L8

消息的 Markdown 渲染使用我另一個項目的 [project](https://github.com/yym68686/md2tgmd)。

## Star 歷史

<a href="https://github.com/yym68686/ChatGPT-Telegram-Bot/stargazers">
        <img width="500" alt="Star 歷史圖表" src="https://api.star-history.com/svg?repos=yym68686/ChatGPT-Telegram-Bot&type=Date">
</a>