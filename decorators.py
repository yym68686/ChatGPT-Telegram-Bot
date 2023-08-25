from md2tgmd import escape

# 判断参数是否为三个
def check_qa_Number_of_parameters(func):
    def wrapper(*args, **kwargs):
        if (len(args[1].args) != 2):
            message = (
                f"格式错误哦~，需要两个参数，注意sitemap.xml、问题之间的空格\n\n"
                f"请输入 `/qa sitemap.xml链接 要问的问题`\n\n"
                f"例如sitemap.xml链接为 https://abc.com/sitemap.xml，问题是 蘑菇怎么分类？\n\n"
                f"则输入 `/qa https://abc.com/sitemap.xml 蘑菇怎么分类？`\n\n"
                f"问题务必不能有空格，👆点击上方命令复制格式\n\n"
            )
            args[1].bot.send_message(chat_id=args[0].effective_chat.id, text=escape(message), parse_mode='MarkdownV2')
            return
        return func(*args, **kwargs)
    return wrapper