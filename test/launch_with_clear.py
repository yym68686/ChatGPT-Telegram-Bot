import os
import subprocess
import sys

# 清理终端
subprocess.call('clear' if os.name == 'posix' else 'cls', shell=True)

# 运行主程序，使用当前正在执行此脚本的 Python 解释器
os.system(f'{sys.executable} bot.py')