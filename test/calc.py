import re
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

banner = "@yym68686"

buttons = [
    [
        InlineKeyboardButton("DEL", callback_data="DEL"),
        InlineKeyboardButton("AC", callback_data="AC"),
    ],
    [
        InlineKeyboardButton("(", callback_data="("),
        InlineKeyboardButton(")", callback_data=")"),
    ],
    [
        InlineKeyboardButton("7", callback_data="7"),
        InlineKeyboardButton("8", callback_data="8"),
        InlineKeyboardButton("9", callback_data="9"),
        InlineKeyboardButton("/", callback_data="/"),
    ],
    [
        InlineKeyboardButton("4", callback_data="4"),
        InlineKeyboardButton("5", callback_data="5"),
        InlineKeyboardButton("6", callback_data="6"),
        InlineKeyboardButton("*", callback_data="*"),
    ],
    [
        InlineKeyboardButton("1", callback_data="1"),
        InlineKeyboardButton("2", callback_data="2"),
        InlineKeyboardButton("3", callback_data="3"),
        InlineKeyboardButton("-", callback_data="-"),
    ],
    [
        InlineKeyboardButton(".", callback_data="."),
        InlineKeyboardButton("0", callback_data="0"),
        InlineKeyboardButton("=", callback_data="="),
        InlineKeyboardButton("+", callback_data="+"),
    ],
]


def calcExpression(text):
    try:
        return float(eval(text))
    except (SyntaxError, ZeroDivisionError):
        return ""
    except TypeError:
        return float(eval(text.replace('(', '*(')))
    except Exception as e:
        logger.error(e, exc_info=True)
        return ""


async def button_press(update, context):
    """Function to handle the button press"""
    callback_query = update.callback_query
    await callback_query.answer()
    text = callback_query.message.text.split("\n")[0].strip().split("=")[0].strip()
    text = '' if banner in text else text
    data = callback_query.data
    inpt = text + data
    result = ''
    if data == "=" and text:
        result = calcExpression(text)
        text = ""
    elif data == "DEL" and text:
        text = text[:-1]
    elif data == "AC":
        text = ""
    else:
        dot_dot_check = re.findall(r"(\d*\.\.|\d*\.\d+\.)", inpt)
        opcheck = re.findall(r"([*/\+-]{2,})", inpt)
        if not dot_dot_check and not opcheck:
            strOperands = re.findall(r"(\.\d+|\d+\.\d+|\d+)", inpt)
            if strOperands:
                text += data
                print(text)
                result = calcExpression(text)

    text = f"{text:<50}"
    if result:
        if text:
            text += f"\n{result:>50}"
        else:
            text = result
    text += '\n\n' + banner
    try:
        await callback_query.edit_message_text(
            text=text, reply_markup=InlineKeyboardMarkup(buttons)
        )
    except Exception as e:
        logger.info(e)
        pass

async def start_handler(update, context):
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        text=banner, reply_markup=InlineKeyboardMarkup(buttons), quote=True
    )

def get_dispatcher(bot):
    """Create and return dispatcher instances"""
    application.add_handler(CommandHandler("calc", start_handler))
    application.add_handler(CallbackQueryHandler(button_press))

    return dispatcher