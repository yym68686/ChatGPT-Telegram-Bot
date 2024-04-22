import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.plugins import get_search_results

for i in get_search_results("今天的微博热搜有哪些？"):
    print(i)