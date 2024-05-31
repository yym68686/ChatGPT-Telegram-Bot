import os
import subprocess

# 清理终端
subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)

# 运行主程序
os.system('/Users/yanyuming/miniconda3/envs/chatgpt/bin/python bot.py')