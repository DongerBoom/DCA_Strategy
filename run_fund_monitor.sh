#!/bin/bash

# 设置工作目录
cd /home/hank/DCA_Strategy

# 激活 Conda 环境
source /opt/anaconda3/etc/profile.d/conda.sh
conda activate DCA_Strategy

# 运行 Python 程序
python main.py

# 记录运行日志（可选）
python main.py >> /home/hank/DCA_Strategy/logs/fund_monitor.log 2>&1