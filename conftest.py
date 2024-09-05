import sys
import os

# 获取项目根目录的路径
project_root = os.path.dirname(os.path.abspath(__file__))

# 将项目根目录添加到 Python 路径中
sys.path.insert(0, project_root)