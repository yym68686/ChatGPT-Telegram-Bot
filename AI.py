import re
import json
import asyncio
import threading
from config import API, NICK, COOKIES
from telegram import ChatAction
from revChatGPT.V3 import Chatbot as GPT
from EdgeGPT import Chatbot as BingAI, ConversationStyle

class AIBot:
    def __init__(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.LastMessage_id = ''
        self.mess = ''

        if COOKIES:
            self.Bingbot = BingAI(cookies=json.loads(COOKIES))
        if API:
            self.ChatGPTbot = GPT(api_key=f"{API}")

        self.botNick = NICK.lower() if NICK else None
        self.botNicKLength = len(self.botNick) if self.botNick else 0
        print("nick:", self.botNick)

    async def typing(self, update, context):
        context.bot.send_chat_action(chat_id=update.effective_user.id, action=ChatAction.TYPING, timeout=60)
        
    async def getBing(self, message, update, context):
        await self.typing(update, context)
        result = ''
        prompt = ""
        try:
            # creative balanced precise
            result = await self.Bingbot.ask(prompt=prompt + message, conversation_style=ConversationStyle.balanced)
            numMessages = result["item"]["throttling"]["numUserMessagesInConversation"]
            maxNumMessages = result["item"]["throttling"]["maxNumUserMessagesInConversation"]
            print(numMessages, "/", maxNumMessages, end="")
            result = result["item"]["messages"][1]["text"]
            if numMessages == maxNumMessages:
                await Bingbot.reset()
        except Exception as e:
            print('\033[31m')
            print("response_msg", result)
            print("error", e)
            print('\033[0m')
            result = "Bing 出错啦。"
        result = re.sub(r"\[\^\d+\^\]", '', result)
        print(" BingAI", result)
        if self.LastMessage_id == '':
            message = context.bot.send_message(
                chat_id=update.effective_user.id,
                text="▎Bing\n\n" + result + "\n\n",
                # parse_mode=ParseMode.MARKDOWN,
                reply_to_message_id=update.message.message_id,
            )
            self.mess = "▎Bing\n\n" + result + "\n\n"
            self.LastMessage_id = message.message_id
            print("LastMessage_id", self.LastMessage_id)
        else:
            context.bot.edit_message_text(chat_id=update.effective_user.id, message_id=self.LastMessage_id, text=self.mess + "▎Bing\n\n" + result + "\n\n")
            self.LastMessage_id = ''
            self.mess = ''
    
    async def resetBing(self):
        await self.Bingbot.reset()
    
    def getChatGPT(self, message, update, context):
        result = ''
        try:
            for data in self.ChatGPTbot.ask(message):
                result += data
        except Exception as e:
            print('\033[31m')
            print("response_msg", result)
            print("error", e)
            print('\033[0m')
            result = "ChatGPT 出错啦。"
        print("ChatGPT", result)
        if self.LastMessage_id == '':
            message = context.bot.send_message(
                chat_id=update.effective_user.id,
                text="▎ChatGPT3.5\n\n" + result + "\n\n",
                reply_to_message_id=update.message.message_id,
            )
            self.LastMessage_id = message.message_id
            self.mess = "▎ChatGPT3.5\n\n" + result + "\n\n"
            print("LastMessage_id", self.LastMessage_id)
        else:
            context.bot.edit_message_text(chat_id=update.effective_user.id, message_id=self.LastMessage_id, text=self.mess + "▎ChatGPT3.5\n\n" + result + "\n\n")
            self.LastMessage_id = ''
            self.mess = ''

    def getResult(self, update, context):
        print("\033[32m", update.effective_user.username, update.effective_user.id, update.message.text, "\033[0m")
        chat_content = update.message.text if NICK is None else update.message.text[self.botNicKLength:].strip() if update.message.text[:self.botNicKLength].lower() == self.botNick else None
        if COOKIES:
            _thread = threading.Thread(target=self.loop.run_until_complete, args=(self.getBing(chat_content, update, context),))
            _thread.start()
        if API:
            self.getChatGPT(chat_content, update, context)
    
    def reset_chat(self, update, context):
        if API:
            self.ChatGPTbot.reset()
        if COOKIES:
            self.loop.run_until_complete(self.resetBing())
        context.bot.send_message(
            chat_id=update.effective_user.id,
            text="重置成功！",
        )
        self.LastMessage_id = ''
        self.mess = ''