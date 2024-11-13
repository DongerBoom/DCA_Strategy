# 基金相关配置
FUND_CODES = {"040046", "050025"}
GROSS_PRICE_DEC = 0.05  # 总跌幅阈值
SINGLE_PRICE_DEC = 0.01  # 单日跌幅阈值

# 通知相关配置
PUSHPLUS_TOKEN = ''
SEND_NORMAL_STATUS = False  # 控制是否发送正常状态的通知
ERROR_THRESHOLD = 5  # 连续错误阈值

# 文件路径配置
ALERT_HISTORY_FILE = 'alert_history.json'
ERROR_HISTORY_FILE = 'error_history.json'

# 每日汇总配置
DAILY_SUMMARY_HOUR = 20  # 每晚8点发送汇总
DAILY_SUMMARY_FILE = 'daily_summary.json'