```markdown
# ChatGPT Telegram Bot

加入 [Telegram 群組](https://t.me/+_01cz9tAkUc1YzZl) 以分享您的使用經驗或回報錯誤。

[English](./README.md) | [Simplified Chinese](./README.zh-CN.md) | [Traditional Chinese](./README.zh-TW.md)

## ✨ 功能

✅ 支援 ChatGPT 和 GPT4 API

✅ 支援使用 DuckDuckGo 和 Google🔍 進行線上搜尋。默認提供 DuckDuckGo 搜尋，使用者需自行申請 Google 搜尋的官方 API。可提供 GPT 以前無法回答的即時資訊，如微博熱搜、某地天氣、某人或新聞的進展等。

✅ 支援基於嵌入式向量數據庫的文檔問答。在搜索中，對於搜尋的 PDF，將執行 PDF 文檔的自動向量語義搜索，並基於向量數據庫提取相關內容。支援使用 "qa" 命令對 "sitemap.xml" 文件進行整個網站的向量化，並基於向量數據庫回答問題，特別適用於一些項目的文檔網站和維基網站。

✅ 支援在聊天窗口通過 "info" 命令在 GPT3.5、GPT4 和其他模型之間切換

✅ 異步處理消息，多線程回答問題，支援隔離對話，不同使用者有不同對話

✅ 支援消息的精確 Markdown 渲染，使用我的另一個 [項目](https://github.com/yym68686/md2tgmd)

✅ 支援流式輸出，實現打字機效果

✅ 支援白名單功能，防止濫用和信息洩漏

✅ 跨平臺，隨時隨地通過 Telegram 打破知識障礙

✅ 支援一鍵 Zeabur、Replit 部署，真正的零成本，白痴部署，並支援 kuma 防止休眠。同時支援 Docker、fly.io 部署

## 環境變量

| 變量名稱                | 說明                                                         |
| ---------------------- | ------------------------------------------------------------ |
| **BOT_TOKEN (必填)**    | Telegram 機器人令牌。在 [BotFather](https://t.me/BotFather) 上創建機器人以獲取 BOT_TOKEN。 |
| **WEB_HOOK (必填)**     | 每當 Telegram 機器人接收到用戶消息時，消息將被傳遞到 WEB_HOOK，機器人將在這裡聽取並及時處理接收到的消息。 |
| **API (必填)**          | OpenAI 或第三方 API 金鑰。                                   |
| API_URL (可選)          | 如果您使用 OpenAI 官方 API，則不需要設置此項。如果使用第三方 API，則需要填寫第三方代理網站。默認值為：https://api.openai.com/v1/chat/completions |
| GPT_ENGINE (可選)       | 設置默認的 QA 模型；默認值為：`gpt-3.5-turbo`。該項目可以使用機器人的 "info" 命令自由切換，原則上不需要設置。 |
| NICK (可選)             | 默認為空，NICK 是機器人的名稱。僅當用戶輸入的消息以 NICK 開頭時，機器人才會回應，否則機器人將對所有消息作出回應。特別是在群聊中，如果沒有 NICK，機器人將回復所有消息。 |
| PASS_HISTORY (可選)     | 默認為 true。機器人將記住對話歷史，並在下次回復時考慮上下文。如果設置為 false，機器人將忘記對話歷史，並僅考慮當前對話。 |
| GOOGLE_API_KEY (可選)   | 如果需要使用 Google 搜尋，則需要設置。如果未設置此環境變量，機器人將默認提供 duckduckgo 搜尋。在 Google Cloud 的 [APIs & Services](https://console.cloud.google.com/apis/api/customsearch.googleapis.com) 中創建憑證，API 金鑰將在憑證頁面上顯示為 GOOGLE_API_KEY。Google 搜尋每天可查詢 100 次，對於輕度使用完全足夠。當達到使用限制時，機器人將自動關閉 Google 搜尋。 |
| GOOGLE_CSE_ID (可選)    | 如果需要使用 Google 搜尋，則需要與 GOOGLE_API_KEY 一同設置。在 [Programmable Search Engine](https://programmablesearchengine.google.com/) 中創建搜索引擎，搜索引擎 ID 是 GOOGLE_CSE_ID 的值。 |
| whitelist (可選)       | 設置哪些用戶可以