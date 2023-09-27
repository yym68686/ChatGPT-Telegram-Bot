# ChatGPT Telegram Bot

加入 [Telegram Group](https://t.me/+_01cz9tAkUc1YzZl) 聊天來分享您的使用體驗或回報問題。

[英文版](./README.md) | [簡體中文版](./README.zh-CN.md) | [繁體中文版](./README.zh-TW.md)

## ✨ 功能

✅ 支持 ChatGPT 和 GPT4 API

✅ 支持使用 DuckDuckGo 和 Google🔍 進行在線搜索。默認提供 DuckDuckGo 搜索，用戶需申請 Google 搜索的官方 API。它可提供 GPT 以前回答不了的即時信息，如今日微博熱搜，某個地方的天氣，以及某個人或新聞的進展情況。

✅ 基於嵌入式向量數據庫的文檔問答支持。在搜索中，對於搜索到的 PDF，會自動進行 PDF 文檔的向量語義搜索，並基於向量數據庫提取與 PDF 相關的內容。支持使用“qa”命令對具有“sitemap.xml”文件的整個網站進行向量化，並基於向量數據庫回答問題，特別適用於一些項目的文檔網站和 wiki 網站。

✅ 通過聊天窗口中的“info”命令支持 GPT3.5、GPT4 和其他模型之間的切換。

✅ 異步處理消息，多線程回答問題，支持獨立對話，不同的用戶有不同的對話氛圍。

✅ 支持準確的消息 Markdown 渲染，採用我的另一個 [項目](https://github.com/yym68686/md2tgmd)。

✅ 支持流式輸出，實現打字機效果。

✅ 支持白名單功能以防止濫用和信息洩露。

✅ 跨平台，在 Telegram 上隨時隨地打破知識障礙。

✅ 支持一鍵 Zeabur、Replit 部署，真正的零成本、白痴式部署，並支持 kuma 抗性睡眠。還支持 Docker、fly.io 部署。

## 環境變量

| 變量名稱             | 註釋                                                         |
| -------------------- | ------------------------------------------------------------ |
| **BOT_TOKEN (required)** | Telegram 機器人 Token。在 [BotFather](https://t.me/BotFather) 上創建一個機器人以獲取 BOT_TOKEN。 |
| **WEB_HOOK (required)**  | 當 Telegram 機器人接收到用戶消息時，消息將被傳遞到 WEB_HOOK，機器人會聽取消息，及時處理接收到的消息。 |
| **API (required)**       | OpenAI 或第三方 API 密鑰。                                 |
| API_URL(optional)       | 如果使用 OpenAI 官方 API，不需要設置此項。如果使用第三方 API，需要填寫第三方代理網站。默認值為：https://api.openai.com/v1/chat/completions |
| GPT_ENGINE (optional)    | 設置默認 QA 模型；默認值為“gpt-3.5-turbo”。可以使用機器人的“info”命令自由切換此項目，原則上不需要設置。 |
| NICK (optional)          | 默認值為空，NICK 是機器人的名字。當用戶輸入的消息以 NICK 開頭時，機器人只會回復該消息，否則機器人會回復所有消息。尤其是在群聊中，如果沒有 NICK，機器人將回復所有消息。 |
| PASS_HISTORY (optional)  | 默認值為 true。機器人會記住對話歷史，並在下次回覆時考慮上下文。如果設置為 false，機器人將忘記對話歷史，並僅考慮當前對話。|
| GOOGLE_API_KEY (optional)| 如果需要使用 Google 搜索，您需要設置它。如果不設置此環境變量，機器人將默認提供 duckduckgo 搜索。在 Google Cloud 的 [APIs ＆ Services](https://console.cloud.google.com/apis/api/customsearch.googleapis.com) 中創建認證，API 密鑰將在認證頁面上的 GOOGLE_API_KEY 上。Google 搜索可以查詢 100 次，這很足夠輕量級使用。當使用次數限制已達到時，機器人將自動關閉 Google 搜索。 |
| GOOGLE_CSE_ID (optional) | 如果需要使用 Google 搜索，您需要與 GOOGLE_API_KEY 一起設置。在 [Programmable Search Engine](https://programmablesearchengine.google.com/) 中創建一個搜索引擎，其中搜索引擎 ID 是 GOOGLE_CSE_ID 的值。 |
| whitelist (optional)     | 設置哪些用戶可以訪問機器人，並將授權使用機器人的用戶 ID 與 ',' 相連接。默認值為 "None"，這意味著機器人對所有人開放。 |

## Zeabur 遠程部署（建議）

一鍵部署：

[![在 Zeabur 上部署](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686)

如果您需要後續功能更新，建議使用以下部署方法：

首先，先 fork 這個庫，然後在 [Zeabur](https://zeabur.com) 上註冊。免費額度足夠輕量使用。從自己的 Github 倉庫導入，設置域名（必須與 WEB_HOOK 一致）和環境變量，然後重新部署。如果需要後續的功能更新，只需將此庫同步到自己的庫並在 Zeabur 中重新部署即可獲取最新功能。

## Replit 遠程部署

[![Repl.it 上的運行](https://replit.com/badge/github/yym68686/ChatGPT-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Telegram-Bot)

導入 Github 倉庫後，設置運行命令

```bash
pip install -r requirements.txt > /dev/null && python3 main.py
```

選擇工具側欄中的 Secrets，添加機器人所需的環境變量，其中：

- WEB_HOOK: Replit將自動分配一個域名給您，填入 `https://appname.username.repl.co`
- 記得打開“Always On”

單擊屏幕頂部的運行按鈕以運行機器人。

## fly.io 遠程部署

官方文檔：https://fly.io/docs/

使用 Docker 鏡像部署 fly.io 應用程序

```bash
flyctl launch --image yym68686/chatgpt:1.0
```

在提示信息中輸入應用程序的名稱，並選擇放棄初始化 Postgresql 或 Redis。

按照提示進行部署。在官方控制面板中將提供次級域名，可用於訪問服務。

設置環境變量

```bash
flyctl secrets set WEB_HOOK=https://flyio-app-name.fly.dev/
flyctl secrets set BOT_TOKEN=bottoken
flyctl secrets set API=
# optional
flyctl secrets set NICK=javis
```

查看所有的環境變量

```bash
flyctl secrets list
```

刪除環境變量

```bash
flyctl secrets unset MY_SECRET DATABASE_URL
```

ssh 到 fly.io 容器中

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

或者，如果您想使用 Docker Compose，這裡有一個 docker-compose.yml 的示例：

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

將 Docker 鏡像打包到庫中並上傳到 Docker Hub

```bash
docker build --no-cache -t chatgpt:1.0 -f Dockerfile.build --platform linux/amd64 .
docker tag chatgpt:1.0 yym68686/chatgpt:1.0
docker push yym68686/chatgpt:1.0
```

## 參考文獻

參考項目:

https://core.telegram.org/bots/api

https://github.com/acheong08/ChatGPT

https://github.com/franalgaba/chatgpt-telegram-bot-serverless

https://github.com/gpchelkin/scdlbot/blob/d64d14f6c6d357ba818e80b8a0a9291c2146d6fe/scdlbot/__main__.py#L8

使用的消息的 Markdown 渲染是我的另一個 [項目](https://github.com/yym68686/md2tgmd)。

## 星星記錄

<a href="https://github.com/yym68686/ChatGPT-Telegram-Bot/stargazers">
        <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=yym68686/ChatGPT-Telegram-Bot&type=Date">
</a>