import re
import json
import threading
from md2tgmd import escape
from runasync import run_async
from config import API, NICK, COOKIES
from revChatGPT.V3 import Chatbot as GPT
from telegram.constants import ChatAction
from EdgeGPT import Chatbot as BingAI, ConversationStyle

class AIBot:
    def __init__(self):
        self.LastMessage_id = ''
        self.mess = ''

        self.bingcookie = COOKIES

        if self.bingcookie:
            try:
                self.Bingbot = BingAI(cookies=json.loads(self.bingcookie))
            except Exception as e:
                print('\033[31m')
                print("Bing 登陆失败！请更换 COOKIES")
                print("error", e)
                print('\033[0m')
                self.bingcookie = None
        if API:
            self.ChatGPTbot = GPT(api_key=f"{API}")

        self.botNick = NICK.lower() if NICK else None
        self.botNicKLength = len(self.botNick) if self.botNick else 0
        print("nick:", self.botNick)

    async def getBing(self, message, update, context):
        result = ''
        prompt = ""
        try:
            # creative balanced precise
            result = await self.Bingbot.ask(prompt=prompt + message, conversation_style=ConversationStyle.creative)
            numMessages = result["item"]["throttling"]["numUserMessagesInConversation"]
            maxNumMessages = result["item"]["throttling"]["maxNumUserMessagesInConversation"]
            print(numMessages, "/", maxNumMessages, end="")
            result = result["item"]["messages"][1]["text"]
            if numMessages == maxNumMessages:
                await self.Bingbot.reset()
        except Exception as e:
            print('\033[31m')
            print("response_msg", result)
            print("error", e)
            print('\033[0m')
            numMessages = 0
            maxNumMessages = 0
            result = "实在不好意思，我现在无法对此做出回应。 要不我们换个话题？"
            await self.Bingbot.reset()
        result = re.sub(r"\[\^\d+\^\]", '', result)
        print(" BingAI", result)
        if self.LastMessage_id == '':
            message = await context.bot.send_message(
                chat_id=update.message.chat_id,
                text=escape(f"🤖️ Bing {numMessages} / {maxNumMessages} \n\n" + result),
                parse_mode='MarkdownV2',
                reply_to_message_id=update.message.message_id,
            )
            self.mess = f"🤖️ Bing {numMessages} / {maxNumMessages} \n\n" + result
            if self.bingcookie and API:
                self.LastMessage_id = message.message_id
        else:
            await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=self.LastMessage_id, text=escape(self.mess + f"\n\n\n🤖️ Bing {numMessages} / {maxNumMessages} \n\n" + result), parse_mode='MarkdownV2')
            self.LastMessage_id = ''
            self.mess = ''
    
    async def resetBing(self):
        await self.Bingbot.reset()
    
    async def getChatGPT(self, message, update, context):
        result = ''
        try:
            result = self.ChatGPTbot.ask(message)
        except Exception as e:
            print('\033[31m')
            print("response_msg", result)
            print("error", e)
            print('\033[0m')
            if "overloaded" in str(e):
                result = "OpenAI 服务器过载。"
            else:
                result = "ChatGPT 出错啦。"
            self.ChatGPTbot.reset()
        print("ChatGPT", result)
        if self.LastMessage_id == '':
            message = await context.bot.send_message(
                chat_id=update.message.chat_id,
                text=escape("🤖️ ChatGPT3.5\n\n" + result),
                parse_mode='MarkdownV2',
                reply_to_message_id=update.message.message_id,
            )
            if self.bingcookie and API:
                self.LastMessage_id = message.message_id
            self.mess = "🤖️ ChatGPT3.5\n\n" + result
        else:
            await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=self.LastMessage_id, text=escape(self.mess + "\n\n\n🤖️ ChatGPT3.5\n\n" + result), parse_mode='MarkdownV2')
            self.LastMessage_id = ''
            self.mess = ''

    async def getResult(self, update, context):
        await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        self.LastMessage_id = ''
        print("\033[32m", update.effective_user.username, update.effective_user.id, update.message.text, "\033[0m")
        chat_content = update.message.text if NICK is None else update.message.text[self.botNicKLength:].strip() if update.message.text[:self.botNicKLength].lower() == self.botNick else None
        if self.bingcookie and chat_content:
            _thread = threading.Thread(target=run_async, args=(self.getBing(chat_content, update, context),))
            _thread.start()
        if API and chat_content:
            await self.getChatGPT(chat_content, update, context)

    async def reset_chat(self, update, context):
        if API:
            self.ChatGPTbot.reset()
        if self.bingcookie:
            await self.resetBing()
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="重置成功！",
        )
        self.LastMessage_id = ''
        self.mess = ''

    async def en2zhtranslator(self, update, context):
        prompt = "I want you to act as a chinese translator. I will speak to you in any language and you will detect the language, translate it and answer in the corrected and improved version of my text, in Chinese. Keep the meaning same, but make them more literary. I want you to only reply the correction, the improvements and nothing else, do not write explanations. My first sentence is \""
        if len(context.args) > 0:
            message = ' '.join(context.args)
            chat_content = prompt + message + '"'
            print("en2zh", message)
            if API and message:
                await self.getChatGPT(chat_content, update, context)
                self.LastMessage_id = ''
                self.mess = ''
        else:
            message = await context.bot.send_message(
                chat_id=update.message.chat_id,
                text="请在命令后面放入要翻译的文本。",
                parse_mode='MarkdownV2',
                reply_to_message_id=update.message.message_id,
            )