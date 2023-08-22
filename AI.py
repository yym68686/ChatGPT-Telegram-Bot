import re
from md2tgmd import escape
from config import API, NICK, API4, PASS_HISTORY
from revChatGPT.V3 import Chatbot as GPT
from telegram.constants import ChatAction

class AIBot:
    def __init__(self):
        self.systemprompt = "You are ChatGPT, a large language model trained by OpenAI. Knowledge cutoff: 2021-09. Current date: [ Current Date ]"
        self.api = API
        self.api4 = API4
        if self.api:
            self.ChatGPTbot = GPT(api_key=f"{self.api}")
        if self.api4:
            self.ChatGPT4bot = GPT(api_key=f"{self.api4}", engine="gpt-4-0613")

        self.botNick = NICK.lower() if NICK else None
        self.botNicKLength = len(self.botNick) if self.botNick else 0
        print("nick:", self.botNick)
    
    async def getChatGPT(self, title, robot, message, update, context):
        result = title
        text = message
        modifytime = 0
        lastresult = ''
        message = await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="思考中💭",
            parse_mode='MarkdownV2',
            reply_to_message_id=update.message.message_id,
        )
        messageid = message.message_id
        try:
            for data in robot.ask_stream(text, convo_id=str(update.message.chat_id), pass_history=PASS_HISTORY):
                result = result + data
                tmpresult = result
                modifytime = modifytime + 1
                if re.sub(r"```", '', result).count("`") % 2 != 0:
                    tmpresult = result + "`"
                if result.count("```") % 2 != 0:
                    tmpresult = result + "\n```"
                if modifytime % 12 == 0 and lastresult != tmpresult:
                    await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=messageid, text=escape(tmpresult), parse_mode='MarkdownV2')
                    lastresult = tmpresult
        except Exception as e:
            print('\033[31m')
            print("response_msg", result)
            print("error", e)
            print('\033[0m')
            if self.api:
                robot.reset(convo_id=str(update.message.chat_id), system_prompt=self.systemprompt)
            if "You exceeded your current quota, please check your plan and billing details." in str(e):
                print("OpenAI api 已过期！")
                await context.bot.delete_message(chat_id=update.message.chat_id, message_id=messageid)
                messageid = ''
                self.api = ''
            result += f"`出错啦！{e}`"
        print(result)
        if lastresult != result and messageid:
            await context.bot.edit_message_text(chat_id=update.message.chat_id, message_id=messageid, text=escape(result), parse_mode='MarkdownV2')

    async def getResult(self, update, context):
        await context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        print("\033[32m", update.effective_user.username, update.effective_user.id, update.message.text, "\033[0m")
        chat_content = update.message.text if NICK is None else update.message.text[self.botNicKLength:].strip() if update.message.text[:self.botNicKLength].lower() == self.botNick else None
        if self.api and chat_content:
            await self.getChatGPT("`🤖️ gpt-3.5`\n\n", self.ChatGPTbot, chat_content, update, context)

    async def reset_chat(self, update, context):
        if self.api:
            self.ChatGPTbot.reset(convo_id=str(update.message.chat_id), system_prompt=self.systemprompt)
        if self.api4:
            self.ChatGPT4bot.reset(convo_id=str(update.message.chat_id), system_prompt=self.systemprompt)
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="重置成功！",
        )