# ChatGPT Telegram Bot

加入 [Telegram 群組](https://t.me/+_01cz9tAkUc1YzZl) 討論，分享您的使用體驗或回報錯誤。

[英文](./README.md) | [簡體中文](./README.zh-CN.md) | [繁體中文](./README.zh-TW.md)

## ✨ 功能

✅ 支援 ChatGPT 和 GPT4 API

✅ 支援使用 DuckDuckGo 和 Google 進行線上搜尋🔍。默認提供 DuckDuckGo 搜尋，使用者需自行申請 Google 搜尋的官方 API，可以提供 GPT 以前無法回答的即時資訊，如微博熱搜、今天某地天氣、某人或新聞的進展等。

✅ 支援基於嵌入式向量數據庫的文件問答。在搜索中，針對搜索到的 PDF 文件，執行 PDF 文檔的自動向量語義搜索，並基於向量數據庫提取與 PDF 相關的內容。支援使用 "qa" 命令對整個網站進行向量化，使用 "sitemap.xml" 文件，並基於向量數據庫回答問題，尤其適用於某些專案的文檔網站和 Wiki 網站。

✅ 支援在聊天視窗中通過 "info" 命令切換 GPT3.5、GPT4 和其他模型

✅ 異步處理消息，多線程回答問題，支援隔離對話，不同使用者有不同對話

✅ 支援精確的消息 Markdown 渲染，使用我的另一個 [專案](https://github.com/yym68686/md2tgmd)

✅ 支援串流輸出，實現打字機效果

✅ 支援白名單，防止濫用和信息洩露

✅ 跨平台，隨時隨地通過 Telegram 打破知識障礙

✅ 支援一鍵 Zeabur、Replit 部署，真正零成本，傻瓜部署，支援 Docker、fly.io 部署

## 環境變數

| 變數名稱                | 說明                                                         |
| ---------------------- | ------------------------------------------------------------ |
| **BOT_TOKEN (必需)**   | Telegram 機器人令牌。在 [BotFather](https://t.me/BotFather) 上創建機器人以獲得 BOT_TOKEN。 |
| **WEB_HOOK (必需)**    | 每當 Telegram 機器人收到用戶消息，消息將被傳遞到 WEB_HOOK，機器人將在及時處理接收到的消息時監聽它。 |
| **API (必需)**         | OpenAI 或第三方 API 金鑰。                                 |
| API_URL (可選)         | 如果您使用 OpenAI 的官方 API，您不需要設置這個。如果您使用第三方 API，您需要填寫第三方代理網站。默認值為: https://api.openai.com/v1/chat/completions |
| GPT_ENGINE (可選)      | 設置默認的 QA 模型；默認值為：`gpt-3.5-turbo`。這個項目可以使用機器人的 "info" 命令自由切換，原則上不需要設置。 |
| NICK (可選)           | 默認為空，NICK 是機器人的名稱。只有在用戶輸入的消息以 NICK 開頭時，機器人才會回應，否則機器人將回應任何消息。特別是在群組聊天中，如果沒有 NICK，機器人將回應所有消息。 |
| PASS_HISTORY (可選)   | 默認為 true。機器人會記住對話歷史，並在下次回應時考慮上下文。如果設置為 false，機器人將忘記對話歷史，只考慮當前對話。 |
| GOOGLE_API_KEY (可選) | 如果需要使用 Google 搜尋，您需要設置它。如果不設置這個環境變數，機器人將默認提供 DuckDuckGo 搜尋。在 Google Cloud 的 [APIs & Services](https://console.cloud.google.com/apis/api/customsearch.googleapis.com) 中創建憑證，API 金鑰將在憑證頁面上的 GOOGLE_API_KEY。Google 搜尋可以每天查詢 100 次，對於輕度使用完全足夠。當使用限制已達到時，機器人將自動關閉 Google 搜尋。 |
| GOOGLE_CSE_ID (可選)  | 如果需要使用 Google 搜尋，您需要與 GOOGLE_API_KEY 一起設置它。在 [Programmable Search Engine](https://programmablesearchengine.google.com/) 中創建搜索引擎，搜索引擎 ID 就是 GOOGLE_CSE_ID 的值。 |
| 白名單 (可選)        | 設定可以訪問機