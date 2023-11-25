# ChatGPT Telegram 機器人

加入 [Telegram 群組](https://t.me/+_01cz9tAkUc1YzZl) 進行用戶體驗分享或回報錯誤。

[英文](./README.md) | [簡體中文](./README.zh-CN.md) | [繁體中文](./README.zh-TW.md)

## ✨ 功能

✅ 支援 GPT3.5 和 GPT4/GPT4 Turbo API，DALLE 3

✅ 支援使用 duckduckgo 和 Google🔍 進行線上搜索。默認提供 DuckDuckGo 搜索，Google 搜索需要用戶申請官方 API。它能提供 GPT 以前無法回答的實時信息，如微博熱搜、某地天氣、某人或新聞的進展等。

✅ 支援基於嵌入式向量數據庫的文檔 QA。在搜索中，對於搜索到的 PDF，將執行 PDF 文檔的自動向量語義搜索，並基於向量數據庫提取 PDF 相關內容。支援使用 "qa" 命令將整個網站向量化，使用 "sitemap.xml" 文件回答基於向量數據庫的問題，特別適用於一些項目的文檔網站和維基網站。

✅ 通過聊天窗口中的 "info" 命令支援在 GPT3.5、GPT4 和其他模型之間切換

✅ 異步處理消息，多線程回答問題，支援隔離對話，不同用戶