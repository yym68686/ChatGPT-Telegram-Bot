# ChatGPT Telegram Bot

加入 [Telegram 群組](https://t.me/+_01cz9tAkUc1YzZl) 分享您的使用經驗或報告錯誤。

[英文](./README.md)|[簡體中文](./README.zh-CN.md)|[繁體中文](./README.zh-TW.md)

## ✨ 特點

✅ 支援 ChatGPT 和 GPT4 API

✅ 支援使用 DuckDuckGo 和 Google🔍 進行在線搜索。預設提供 DuckDuckGo 搜索，而 Google 搜索的官方 API 需要用戶申請。它可以提供 GPT 之前無法回答的即時資訊，例如微博熱搜、今天特定地點的天氣以及特定人員或新聞的進度。

✅ 支援基於內置向量數據庫的文檔 QA。在搜索中，對於被搜索的 PDF，會對 PDF 文檔進行自動向量語義搜索，並提取與向量數據庫相關的內容。支援使用 “qa” 命令向量化 “sitemap.xml” 文件中的整個網站，並在向量數據庫的基礎上回答問題，尤其適用於某些專案的文檔網站和 Wiki 網站。​

✅ 支援透過聊天窗口中的 “info” 命令在 GPT3.5、GPT4 和其他模型之間進行切換

✅ 非同步處理訊息，多線程回答問題，支援獨立對話，並使不同的用戶擁有不同的對話​

✅ 支援精確的 markdown 渲染消息，使用我的另一個 [項目](https://github.com/yym68686/md2tgmd)

✅ 支援流輸出，實現打字機效果

✅ 支援白名單，以防止濫用和信息泄露

✅ 跨平台，在 Telegram 上隨時隨地打破知識障礙

✅ 支援一鍵 Zeabur、Replit 部署，真正的零成本、白癡式部署，支援 kuma 防睡眠。還支援 Docker、fly.io 部署

## 環境變量

| 變量名稱                  | 評論                                                         |
| ------------------------- | ------------------------------------------------------------ |
| **BOT_TOKEN（必填）**          | Telegram 機器人 token。在 [BotFather](https://t.me/BotFather) 上創建機器人以獲得 BOT_TOKEN。 |
| **WEB_HOOK（必填）**           | 每當 Telegram 機器人接收到用戶消息，該消息將被傳遞到 WEB_HOOK，機器人將在 WEB_HOOK 上監聽，隨時處理收到的消息。 |
| **API（必填）**                | OpenAI 或第三方 API 金鑰。                                |
| API_URL（可選）            | 如果您使用 OpenAI 的官方 API，則不需要設置此項。如果您使用第三方 API，則需要填寫第三方代理網站。默認為: https://api.openai.com/v1/chat/completions |
| GPT_ENGINE（可選）         | 設置默認 QA 模型；默認為：`gpt-3.5-turbo`。該項可以通過機器人的 “info” 命令自由切換，原則上不需要進行設置。 |
| NICK（可選）               | 預設值為空，NICK 是機器人的名字。當用戶輸入的消息以 NICK 開頭時，機器人只會回應該消息，否則機器人會回應所有消息。尤其在群聊中，如果沒有 NICK，機器人會回應所有消息。 |
| PASS_HISTORY（可選）       | 預設值為 true。機器人記住對話記錄，下一次回答時會考慮上下文。如果設置為 false，機器人會忘記對話記錄，只考慮當前對話。 |
| GOOGLE_API_KEY（可選）     | 如果您需要使用 Google 搜索，您需要進行設置。如果未設置此環境變量，機器人將默認提供 DuckDuckGo 搜索。在 Google Cloud 的 [API 和服務](https://console.cloud.google.com/apis/api/customsearch.googleapis.com) 中創建憑據，API 金鑰在憑據頁面上是 GOOGLE_API_KEY。Google 搜索可以查詢 100 次/日，這對輕度使用者已足夠。當使用限制已到達時，機器人將自動關閉 Google 搜索。 |
| GOOGLE_CSE_ID（可選）      | 如果您需要使用 Google 搜索，您需要與 GOOGLE_API_KEY 一起設置。在 [可編程搜索引擎](https://programmablesearchengine.google.com/) 中創建搜索引擎，其中搜索引擎 ID 是 GOOGLE_CSE_ID 的值。 |
| whitelist（可選）          | 設置哪些用戶可以訪問機器人，並用 “，” 將授權使用機器人的用戶 ID 連接。默認值為 `None`，這意味著機器人對所有人開放。 |

## Zeabur 遠程部署（推薦）

一鍵部署：

[![使用 Zeabur 部署](https://zeabur.com/button.svg)](https://zeabur.com/templates/R5JY5O?referralCode=yym68686)

如果需要後續功能更新，建議使用以下部署方法：

首先 fork 此存儲庫，然後註冊 [Zeabur](https://zeabur.com)。免費額度足以輕鬆使用。從您自己的 Github 存儲庫中進行導入，設置網域名稱（必須與 WEB_HOOK 一致）和環境變量，然後重新部署。如果需要後續功能更新，只需將此存儲庫同步到您自己的存儲庫中，然後在 Zeabur 中重新部署即可獲取最新的功能。

## Replit 遠程部署

[![在 Repl.it 上運行](https://replit.com/badge/github/yym68686/ChatGPT-Telegram-Bot)](https://replit.com/new/github/yym68686/ChatGPT-Telegram-Bot)

將 GitHub 存儲庫導入後，設置運行命令

```bash
pip install -r requirements.txt > /dev/null && python3 main.py
```

在 Tools 側邊欄中選擇 Secrets，添加機械人所需的環境變量，其中：

- WEB_HOOK：Repl.it 將自動為您分配一個網域名稱，填寫 `https://appname.username.repl.co`
- 記住要開啟 “始終運行”

單擊屏幕頂部的運行按鈕運行機械人。

## fly.io 遠程部署

官方文檔: https://fly.io/docs/

使用 Docker 映像部署 fly.io 應用程式

```bash
flyctl launch --image yym68686/chatgpt:1.0
```

輸入應用程式的名稱，並對 Postgresql 或 Redis 進行初始化選擇 No。

按照提示進行部署。在官方控制面板中提供了一個次要域名，可以用於訪問服務。

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
# ssh 鏈接
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
    -e BOT_TOKEN="telegram 機器人 token" \
    -e WEB_HOOK="https://your_host.com/" \
    -e API="" \
    -e API_URL= \
    yym68686/chatgpt:1.0
```

或者如果您想使用 Docker Compose，這裡有一個 docker-compose.yml 的示例：

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

將 Docker 映像打包在存儲庫中並上傳到 Docker Hub

```bash
docker build --no-cache -t chatgpt:1.0 -f Dockerfile.build --platform linux/amd64 .
docker tag chatgpt:1.0 yym68686/chatgpt:1.0
docker push yym68686/chatgpt:1.0
```

## 參考

參考項目：

https://core.telegram.org/bots/api

https://github.com/acheong08/ChatGPT

https://github.com/franalgaba/chatgpt-telegram-bot-serverless

https://github.com/gpchelkin/scdlbot/blob/d64d14f6c6d357ba818e80b8a0a9291c2146d6fe/scdlbot/__main__.py#L8

消息的 markdown 渲染使用了我的另一個 [項目](https://github.com/yym68686/md2tgmd)。

## Star 历史

<a href="https://github.com/yym68686/ChatGPT-Telegram-Bot/stargazers">
        <img width="500" alt="Star History Chart" src="https://api.star-history.com/svg?repos=yym68686/ChatGPT-Telegram-Bot&type=Date">
</a>