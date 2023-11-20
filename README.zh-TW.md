```markdown
# ChatGPT Telegram Bot

加入 [Telegram 群組](https://t.me/+_01cz9tAkUc1YzZl) 聊天，分享您的使用經驗或回報錯誤。

[英文](./README.md) | [簡體中文](./README.zh-CN.md) | [繁體中文](./README.zh-TW.md)

## ✨ 功能

✅ 支援 GPT3.5 和 GPT4/GPT4 Turbo API，以及 DALLE 3

✅ 支援使用 duckduckgo 和 Google🔍 進行在線搜索。默認情況下提供 DuckDuckGo 搜索，使用者需要申請 Google 搜索的官方 API。可以提供 GPT 之前無法回答的實時信息，例如今天的微博熱搜、某地區今天的天氣和某人或新聞的進展。

✅ 支援基於內嵌向量數據庫的文檔 QA。在搜索中，對於搜索的 PDF，將執行 PDF 文檔的自動向量語義搜索，並基於向量數據庫提取與 PDF 相關的內容。支援使用 "qa" 命令將整個網站向量化，使用 "sitemap.xml" 文件，並根據向量數據庫回答問題，特別適用於文檔網站和某些項目的 Wiki 網站。

✅ 通過聊天窗口中的 "info" 命令支援在 GPT3.5、GPT4 和其他模型之間切換

✅ 異步處理消息，多線程回答問題，支援隔離對話，不同用戶有不同的對話

✅ 支援消息的精確 Markdown 渲染，使用我另一個 [項目](https://github.com/yym68686/md2tgmd)

✅ 支援流式輸出，實現打字機效果

✅ 支援白名單功能，防止濫用和信息洩露

✅ 跨平台，在任何地方都可以使用 Telegram 打破知識障礙

✅ 支援一鍵 Zeabur、Replit 部署，真正的零成本，傻瓜部署，並支援 kuma 防睡眠。同時支援 Docker、fly.io 部署

## 環境變量

| 變量名稱                  | 說明                                                         |
| ---------------------- | ------------------------------------------------------------ |
| **BOT_TOKEN (必填)**     | Telegram 機器人令牌。在 [BotFather](https://t.me/BotFather) 上創建機器人以獲取 BOT_TOKEN。 |
| **API (必填)**          | OpenAI 或第三方 API 金鑰。                                   |
| WEB_HOOK                | 當電報機器人收到用戶消息時，消息將傳遞到 WEB_HOOK，機器人將在那裡聽取並及時處理接收到的消息。 |
| API_URL (可選)          | 如果使用 OpenAI 官方 API，則不需要設置此項。如果使用第三方 API，則需要填寫第三方代理網站。默認值為：https://api.openai.com/v1/chat/completions |
| GPT_ENGINE (可選)       | 設置默認的 QA 模型；默認為:`gpt-3.5-turbo`。可以使用機器人的 "info" 命令自由切換此項，原則上無需設置。 |
| NICK (可選)             | 默認為空，NICK 是機器人的名稱。只有當用戶輸入的消息以 NICK 開頭時，機器人才會回應，否則機器人將對所有消息進行回應。特別是在群組聊天中，如果沒有 NICK，機器人將對所有消息進行回應。 |
| PASS_HISTORY (可選)     | 默認為 true。機器人會記住對話歷史並在下次回覆時考慮上下文。如果設置為 false，機器人將忘記對話歷史，只考慮當前對話。 |
| GOOGLE_API_KEY (可選)   | 如果需要使用 Google 搜索，則需要設置此項。如果不設置此環境變量，機器人將默認提供 duckduckgo 搜索。在 Google Cloud 的 [APIs & Services](https://console.cloud.google.com/apis/api/customsearch.googleapis.com) 中創建憑據，API 金鑰將出現在憑據頁面上。Google 搜索每天可以查詢 100 次，對於輕量使用完全足夠。當達到使用限制時，機器人將自動關閉 Google 搜索。 |
| GOOGLE_CSE_ID (可選)    | 如果需要使用 Google 搜索，則需要與 GOOGLE_API_KEY 一起設置此項。在 [Programmable Search Engine](https://programmablesearchengine.google.com/) 中創建搜索引擎，搜索引擎 ID 將是 GOOGLE_CSE_ID 的值。 |
| whitelist (可選)       